"""
The asplain project.
"""

import logging
from typing import Any, List, Optional, Tuple

from clingo import Control, SolveHandle, Symbol
from meta_tools import classic_reify, extend_reification, transform
from meta_tools.extensions import ShowExtension, TagExtension
from meta_tools.utils.theory import extend_with_theory_symbols

from asplain.llm.utils.graph import Graph
from asplain.utils.clingo import (
    assert_no_errors,
    assumptions_as_ic,
    constants_to_args,
    load_encoding,
    symbols_to_prg,
)
from asplain.utils.logging import colored, save_out

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
    constants = constants or {}
    extensions = [
        TagExtension(include_program=True, include_loc=True, include_id=True),
        ShowExtension(),
    ]
    program_str = transform(file_paths, prg, extensions)
    log.debug("Transformed program:\n%s", program_str)
    rsymbols = classic_reify(
        constants_to_args(constants) + ["--preserve-facts=symtab"],
        program_str,
        programs=[("base", []), ("asplain", [])],
    )
    extend_with_theory_symbols(rsymbols)
    reified_prg = "\n".join([f"{str(s)}." for s in rsymbols])
    reified_prg = extend_reification(reified_out_prg=reified_prg, extensions=extensions, clean_output=True)
    save_out("reference_reified.lp", reified_prg)
    return reified_prg


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
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


def set_model_subgraphs_ctl(
    pg: str, ctl: Optional[Control] = None, model_symbols: Optional[List[str]] = None
) -> Control:
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
        log.debug("Setting model symbols: %s", model_symbols)
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


class Foil:
    """
    Class to represent a foil, including the atoms in the foil model,
    the added and removed rules, and the reference atoms.
    Intended to save the result of obtaining foils
    """

    def __init__(
        self,
        foil_atoms: list[str],
        added_rules: list[str],
        removed_rules: list[str],
        reference_atoms: list[str],
        explanation_graph_facts: str = "",
    ) -> None:
        self.foil_atoms = set(foil_atoms)
        self.added_rules = set(added_rules)
        self.removed_rules = set(removed_rules)
        self.reference_atoms = set(reference_atoms)
        self.explanation_graph_facts = explanation_graph_facts

    @classmethod
    def from_explanation_graph(cls, foil_pg: str) -> "Foil":
        """
        Inspect the foil program graph to extract the foil model, added and removed rules.

        Args:
            foil_pg: The program graph of the foil model as a string of facts.

        Returns:
            A tuple containing three lists:
            - foil_atoms: The atoms in the foil model.
            - added_rules: The rules added in the foil model.
            - removed_rules: The rules removed in the foil model.
        """
        ctl = Control()
        ctl.add("base", [], foil_pg)
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            model = handle.model()
            log.debug("Inspecting foil model")
            graph = Graph("".join([str(s) + "." for s in model.symbols(shown=True)]))
            log.debug("Constructed graph")
            added_rules = []
            removed_rules = []
            foil_atoms = []
            reference_atoms = []
            for node in graph._nodes.values():  # pylint: disable=protected-access
                if node.type == "atom" and "foil" in node.models:
                    foil_atoms.append(node.id)
                if node.type == "atom" and "ref" in node.models:
                    reference_atoms.append(node.id)
                if node.programs == set(["ref"]):
                    removed_rules.append(node.tags["first_order"])
                if node.programs == set(["foil"]):
                    added_rules.append(node.tags["first_order"])
        return cls(foil_atoms, added_rules, removed_rules, reference_atoms, foil_pg)  # type: ignore

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Foil):
            return NotImplemented
        return (
            self.foil_atoms == other.foil_atoms
            and self.added_rules == other.added_rules
            and self.removed_rules == other.removed_rules
            and self.reference_atoms == other.reference_atoms
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __hash__(self) -> int:
        return hash(
            (
                frozenset(self.foil_atoms),
                frozenset(self.added_rules),
                frozenset(self.removed_rules),
                frozenset(self.reference_atoms),
            )
        )

    def __repr__(self) -> str:
        return (
            f"Foil(reference_atoms={self.reference_atoms}, "
            f"foil_atoms={self.foil_atoms}, "
            f"added_rules={self.added_rules}, "
            f"removed_rules={self.removed_rules})"
        )

    def print(self) -> None:
        """
        Print the foil model, added and removed rules.
        """
        print(colored("blue", "Foil model (satisfying query): " + " ".join([str(s) for s in self.foil_atoms])))
        if len(self.removed_rules) > 0:
            print(colored("red", "            Removed: " + "\t".join([str(s) for s in self.removed_rules])))
        if len(self.added_rules) > 0:
            print(colored("green", "            Added: " + "\t".join([str(s) for s in self.added_rules])))
