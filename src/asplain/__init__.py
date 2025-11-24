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

from asplain.utils.clingo import assert_no_errors, assumptions_as_ic, constants_to_args, load_encoding, symbols_to_prg
from asplain.utils.logging import save_out

log = logging.getLogger(__name__)


def reify_program(
    file_paths: List[str],
    prg: str = "",
    constants: Optional[dict[str, str]] = None,
) -> str:
    """Reifies a program."""
    extensions = [TagExtension(include_program=True), ShowExtension()]
    program_str = transform(file_paths, prg, extensions)
    rsymbols = classic_reify(
        constants_to_args(constants) + ["--preserve-facts=symtab"],
        program_str,
        programs=[("base", []), ("addable", [])],
    )
    extend_with_theory_symbols(rsymbols)
    reified_prg = "\n".join([f"{str(s)}." for s in rsymbols])
    reified_prg = extend_reification(reified_out_prg=reified_prg, extensions=extensions, clean_output=True)
    save_out(f"reference_reified.lp", reified_prg)
    return reified_prg


def construct_program_graph(
    file_paths: List[str],
    prg: str = "",
    constants: Optional[dict[str, str]] = None,
    assumptions: Optional[List[Tuple[str, bool]]] = None,
    dynamic_tags_prg: Optional[str] = None,
    dynamic_tags_files: Optional[List[str]] = None,
    target_name: str = "reference",
) -> str:
    """Constructs a program graph."""
    constants = constants or {}

    if assumptions is not None:
        prg = prg + assumptions_as_ic(assumptions)
    log.info(f"Reifying program {file_paths} with constants {constants} and assumptions {assumptions}")
    reified_prg = reify_program(file_paths, prg, constants)
    ctl = Control()
    ctl.add("base", [], reified_prg)
    if dynamic_tags_prg:
        ctl.add("tags", [], dynamic_tags_prg)
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
        assert_no_errors(model_symbols)
    return symbols_to_prg(model_symbols)


def set_model_subgraphs_ctl(pg, ctl=None, model_symbols: Optional[List[str]] = None) -> Control:
    """Iterates over model subgraphs."""
    ctl = ctl or Control(["0", f"-c graph=reference"])
    ctl.add("base", [], pg)
    if model_symbols is not None:
        model_prg = "\n".join([f"_model({str(s)})." for s in model_symbols])
        ctl.add("base", [], model_prg)
        load_encoding(ctl, "force-model.lp")

    load_encoding(ctl, "model-subgraph.lp")
    ctl.ground([("base", [])])
    return ctl


def set_foil_ctl(
    reference_pg: str,
    reference_model_pg: Optional[str],
    query_prg: Optional[str] = None,
    distance_prg: Optional[str] = None,
    number_of_foils: int = 1,
) -> Control:
    """Constructs a FOIL."""
    log.info(query_prg)
    ctl = Control([str(number_of_foils), "-c graph=foil"])
    ctl.add("base", [], reference_pg)
    ctl.add("base", [], reference_model_pg or "")
    ctl.add("base", [], query_prg or "")
    ctl.add("base", [], distance_prg or "")
    load_encoding(ctl, "construct-foil.lp")
    load_encoding(ctl, "model-subgraph.lp")
    ctl.ground([("base", [])])
    return ctl


def construct_contrastive(
    reference_pg: str,
    foil_pg_tuple: str,
    reference_model_pg: Optional[str],
    query_prg: Optional[str],
) -> str:
    """Constructs a contrastive explanation."""
    ctl = Control()
    ctl.add("base", [], reference_pg)
    ctl.add("base", [], foil_pg_tuple)
    ctl.add("base", [], reference_model_pg or "")
    ctl.add("base", [], query_prg or "")
    load_encoding(ctl, "construct-contrastive.lp")
    ctl.ground([("base", [])])
    with ctl.solve(yield_=True) as handle:
        model = handle.model()
        model_symbols = model.symbols(shown=True)
        return symbols_to_prg(model_symbols)

    raise RuntimeError("No contrastive explanation could be constructed.")


def contrast(
    number_of_foils: int,
    reference_pg: str,
    reference_model_pg: Optional[str] = None,
    query_prg: Optional[str] = None,
    distance_prg: Optional[str] = None,
    on_contrasttive: Optional[callable] = None,
) -> None:
    ctl = set_foil_ctl(
        reference_pg=reference_pg,
        reference_model_pg=reference_model_pg,
        number_of_foils=number_of_foils,
        query_prg=query_prg,
        distance_prg=distance_prg,
    )
    with ctl.solve(yield_=True) as foil_hnd:
        foil_found = False
        # only iterate the number of explanations wanted
        for foil_model in foil_hnd:
            foil_found = True
            foil_model_pg = symbols_to_prg(foil_model.symbols(shown=True))  # shown should include the foil model and pg
            save_out(f"foil_model_pg_{foil_model.number}.lp", foil_model_pg)

            contrastive_pg = construct_contrastive(
                reference_pg=reference_pg,
                foil_pg_tuple=foil_model_pg,
                reference_model_pg=reference_model_pg,
                query_prg=query_prg,
            )
            save_out(f"contrastive_{foil_model.number}.lp", contrastive_pg)
            if on_contrasttive:
                on_contrasttive(contrastive_pg)

        if not foil_found:
            log.warning("No foil found.")
