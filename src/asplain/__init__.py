"""
The asplain project.
"""

import logging
from importlib.resources import path
from typing import List, Optional, Tuple

from clingo import Control, SolveHandle, Symbol
from meta_tools import classic_reify, extend_reification, transform
from meta_tools.extensions import ShowExtension, TagExtension
from meta_tools.utils.theory import extend_with_theory_symbols

from asplain.utils.clingo import (
    assert_no_errors,
    assumptions_as_ic,
    constants_to_args,
    load_encoding,
    symbols_to_prg,
)
from asplain.utils.logging import save_out

log = logging.getLogger(__name__)


def reify_program(
    file_paths: List[str],
    prg: str = "",
    constants: Optional[dict[str, str]] = None,
) -> str:
    """Reifies a program.
    Args:
        file_paths: List of file paths to load.
        prg: Additional program string to include.
        constants: Constants to pass to clingo.
    Returns:
        The reified program as a string.
    """
    extensions = [
        TagExtension(include_program=True, include_loc=True, include_id=True),
        ShowExtension(),
    ]
    program_str = transform(file_paths, prg, extensions)
    log.debug("Transformed program:\n%s", program_str)
    rsymbols = classic_reify(
        constants_to_args(constants) + ["--preserve-facts=symtab"],
        program_str,
        programs=[("base", []), ("addable", [])],
    )
    extend_with_theory_symbols(rsymbols)
    reified_prg = "\n".join([f"{str(s)}." for s in rsymbols])
    reified_prg = extend_reification(reified_out_prg=reified_prg, extensions=extensions, clean_output=True)
    save_out("reference_reified.lp", reified_prg)
    return reified_prg


# pylint: disable=too-many-arguments
def construct_program_graph(
    file_paths: List[str],
    prg: str = "",
    constants: Optional[dict[str, str]] = None,
    assumptions: Optional[List[Tuple[str, bool]]] = None,
    dynamic_tags_prg: Optional[str] = None,
    dynamic_tags_files: Optional[List[str]] = None,
) -> str:
    """Constructs a program graph
    Args:
        file_paths: List of file paths to load.
        prg: Additional program string to include.
        constants: Constants to pass to clingo.
        assumptions: Assumptions to include as integrity constraints.
        dynamic_tags_prg: Dynamic tags program string to generate tags.
        dynamic_tags_files: List of files to load for dynamic tags.
    Returns:
        The program graph as a string.
    """
    constants = constants or {}

    if assumptions is not None:
        prg = prg + assumptions_as_ic(assumptions)
    log.info(
        "Reifying program %s with constants %s and assumptions %s",
        file_paths,
        constants,
        assumptions,
    )
    reified_prg = reify_program(file_paths, prg, constants)
    ctl = Control()
    ctl.add("base", [], reified_prg)
    if dynamic_tags_prg:
        ctl.add("base", [], dynamic_tags_prg)
    if dynamic_tags_files:
        for file in dynamic_tags_files:
            log.info("Loading dynamic tags file: %s", file)
            ctl.load(file)
    load_encoding(ctl, "reify-to-pg.lp")
    ctl.ground([("base", [])])
    with ctl.solve(yield_=True) as handle:
        model = handle.model()
        if model is None:
            raise RuntimeError("No model found when constructing program graph.")
        model_symbols = model.symbols(shown=True)
        assert_no_errors(list(model_symbols))
    return symbols_to_prg(list(model_symbols))


def set_model_subgraphs_ctl(pg, ctl=None, model_symbols: Optional[List[str]] = None) -> Control:
    """
    Sets the control object for computing model subgraphs.
    Args:
        pg: The program graph string.
        ctl: Optional existing Control object.
        model_symbols: Optional list of model symbols.
    Returns:
        The Control object with the model subgraph encoding loaded and grounded
    """
    ctl = ctl or Control(["0", "-c graph=ref"])
    ctl.add("base", [], pg)
    if model_symbols is not None:
        model_prg = "\n".join([f"model({str(s)})." for s in model_symbols])
        ctl.add("base", [], model_prg)
        load_encoding(ctl, "force-model.lp")

    load_encoding(ctl, "model-subgraph.lp")
    ctl.ground([("base", [])])
    return ctl


def set_foil_ctl(
    pg: str,
    query_prg: Optional[str] = None,
    cost_prg: Optional[str] = None,
    number_of_foils: int = 1,
) -> Control:
    """Constructs a foil to explain a query.
    Args:
        pg: The reference program graph string which might include facts for the reference model graph.
        query_prg: The query program string.
        cost_prg: The distance program string.
        number_of_foils: The number of foils to construct.
    """
    log.debug("Query program : %s", query_prg or "<none>")
    log.debug("Cost program  : %s", cost_prg or "<none>")
    log.debug("Program graph: %s", pg)
    ctl = Control([str(number_of_foils), "-c graph=foil", "--opt-mode=optN"])
    ctl.add("base", [], pg)
    ctl.add("base", [], query_prg or "")
    ctl.add("base", [], cost_prg or "")
    load_encoding(ctl, "construct-foil.lp")
    load_encoding(ctl, "model-subgraph.lp")
    ctl.ground([("base", [])])
    return ctl


def construct_contrastive(
    pg: str,
    query_prg: Optional[str],
) -> str:
    """Constructs a contrastive explanation.
    Args:
        pg: The set of facts defining the reference program graph,
            foil program graph, foil model graph and optionally the reference model graph.
        query_prg: The query program string defined via query/2 facts.
    Returns:
        The contrastive explanation program graph as a string,
        which includes the facts for the input graphs in pg.
    """
    ctl = Control()
    ctl.add("base", [], pg)
    ctl.add("base", [], query_prg or "")
    ctl.ground([("base", [])])
    with ctl.solve(yield_=True) as handle:
        model = handle.model()
        if model is None:
            raise RuntimeError("No contrastive explanation could be constructed.")
        model_symbols = model.symbols(shown=True)
        return symbols_to_prg(list(model_symbols))

    raise RuntimeError("No contrastive explanation could be constructed.")
