import os
import shutil
from importlib.resources import path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from clingexplaid.transformers import RuleIDTransformer
from clingo import Control, Function, Number, Symbol, TheoryTermType
from clingo.script import enable_python

# pylint: disable=E0401
from clingox.reify import ReifiedTheory, ReifiedTheoryTerm, Reifier
from clingox.theory import evaluate, is_operator
from clingraph.clingo_utils import ClingraphContext  # type: ignore
from clingraph.graphviz import compute_graphs, render  # type: ignore
from clingraph.orm import Factbase  # type: ignore

from ..transformers.graph_transformer import GraphTransformer
from ..utils.logging import get_logger
from .base_explainer import Explainer

log = get_logger("main")


def _visit_terms(thy: ReifiedTheory, cb: Callable[[ReifiedTheoryTerm], None]):
    """
    Visit the terms occuring in the theory atoms of the given theory.

    This function does not recurse into terms.
    """
    for atm in thy:
        for elem in atm.elements:
            for term in elem.terms:
                cb(term)
        cb(atm.term)
        guard = atm.guard
        if guard:
            cb(guard[1])


def query_to_pgr(query_include: Sequence[str], query_exclude: Sequence[str]) -> str:
    """
    Convert query include and exclude symbols to a program graph representation.
    """
    pg = ""
    for s in query_include:
        pg += f"query(include,{s}).\n"
    for s in query_exclude:
        pg += f"query(exclude,{s}).\n"
    return pg


def _term_symbols(term: ReifiedTheoryTerm, ret: Dict[int, Symbol]) -> None:
    """
    Represent arguments to theory operators using clingo's `clingo.Symbol`
    class.

    Theory terms are evaluated using `clingox.theory.evaluate_unary` and added
    to the given dictionary using the index of the theory term as key.
    """
    if term.type == TheoryTermType.Function and is_operator(term.name):
        _term_symbols(term.arguments[0], ret)
        if len(term.arguments) >= 2:
            _term_symbols(term.arguments[1], ret)
    elif term.index not in ret:
        ret[term.index] = evaluate(term)


def reify(prg: str = "", files: Sequence[str] = None) -> str:
    """
    Do the reification using clingox Reifier
    """
    symbols: List[Symbol] = []

    ctl = Control(["--warn=none"])
    reifier = Reifier(symbols.append, reify_steps=False)
    ctl.register_observer(reifier)
    ctl.add("base", [], prg)
    if files is not None:
        for f in files:
            ctl.load(f)

    with path("asplain.encodings", "tag_theory.lp") as tag_theory_encoding:
        log.info("Loading encoding: %s", tag_theory_encoding)
        ctl.load(str(tag_theory_encoding))

        ctl.ground([("base", [])])

        theory_symbols: Dict[int, Symbol] = {}
        _visit_terms(ReifiedTheory(symbols), lambda term: _term_symbols(term, theory_symbols))

        for k, v in theory_symbols.items():
            symbols.append(Function("theory_symbol", [Number(k), v]))
        return "\n".join([f"{str(s)}." for s in symbols])


class ContrastiveExplainer(Explainer):
    """
    Explanation class for contrastive explanations.
    """

    def __init__(self, output_dir: str, visualize: bool = True, store: bool = True):
        """
        Create an Asplain instance.

        Args:
            output_dir: Directory where the output files will be stored.
            visualize: Whether to visualize the explanation graphs.
            store: Whether to store the explanation graphs in the output directory.
        """
        self._visualize = visualize
        self._store = store

        # Output directory for intermediate files and images
        self._output_dir = output_dir
        # Remove the directory if it exists, then create it fresh
        if os.path.exists(self._output_dir):
            shutil.rmtree(self._output_dir)
        os.makedirs(self._output_dir, exist_ok=True)

    def assumptions_as_ic(self, assumptions: Sequence[Tuple[Symbol, bool]]) -> str:
        """
        Convert assumptions to integrity constraints.

        Args:
            assumptions: List of assumptions as tuples of (Symbol, bool).

        Returns:
            A string representing the integrity constraints.
        """
        prg = ""
        for s, b in assumptions:
            if b:
                prg += f":- not {str(s)}, &tag_rule{{assume(true)}}.\n"
            else:
                prg += f":- {str(s)}, &tag_rule{{assume(false)}}.\n"
        log.debug("Assumptions as integrity constraints: %s", prg)
        return prg

    def reify(self, files: Sequence[str], assumptions: Sequence[Tuple[Symbol, bool]]) -> str:

        assumptions_as_constraints = self.assumptions_as_ic(assumptions)

        reified_prg = reify(assumptions_as_constraints, files)
        if self._store:
            with open(os.path.join(self._output_dir, "reify.lp"), "w") as f:
                f.write(reified_prg)
                log.info("Reified program saved in " + f.name)
        # if self._visualize:
        #     self.viz_reify(reified_prg)
        return reified_prg

    def generate_pg(self, files: Sequence[str], assumptions: Optional[Sequence[Tuple[Symbol, bool]]] = None):
        if not assumptions:
            assumptions = []
        log.info("-----Reifying program")
        reified_prg = self.reify(files, assumptions)

        log.info("-----Computing PG")
        ctl = Control(arguments=["1", "--warn=none"])
        ctl.add("base", [], reified_prg)
        with path("asplain.encodings", "reify_to_pg.lp") as base_encoding:
            log.info("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))

        ctl.ground([("base", [])])
        pg = ""
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                pg = "\n".join([str(s) + "." for s in m.symbols(shown=True)])
        if not pg:
            log.error("No program graph found")
            return None

        if self._store:
            with open(os.path.join(self._output_dir, "pg.lp"), "w") as f:
                f.write(pg)
                log.info("Program graph saved in " + f.name)

        if self._visualize:
            self.viz_graph(pg, "reference", "Program Graph", file_name="pg", draw_types=["pg"])
        return pg

    def setup_ctl_from_pg(
        self,
        ctl: Control,
        pg: str,
        model_symbols: Sequence[str],
        query_include: Sequence[str],
        query_exclude: Sequence[str],
    ):
        """
        Setup the control object with the program graph and model symbols.

        Args:
            ctl: The control object to setup.
            pg: The program graph as a string of facts
            model_symbols: The symbols of the model to be fixed, this will make sure this model is obtained from the pg.
            query_include: The symbols that must be checked if included in the model.
            query_exclude: The symbols that must be checked if excluded in the model.
        """
        ctl.add("base", [], pg)

        if model_symbols is not None:
            model_prg = "\n".join([f"_model({str(s)})." for s in model_symbols])
            model_prg += "_force_model."
            ctl.add("base", [], model_prg)

        q_prg = query_to_pgr(query_include, query_exclude)
        ctl.add("base", [], q_prg)

        with path("asplain.encodings", "solve_pg.lp") as base_encoding:
            log.info("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))

    def tag_symbols(self, prg: str, tag: str) -> List[Symbol]:
        """ """
        ctl = Control(["--warn=none"])
        ctl.add("base", [], prg)
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                tag_atom = Function(tag, [])
                new_symbols = []
                for s in m.symbols(shown=True):
                    new_s = Function(s.name, s.arguments + [tag_atom])
                    new_symbols.append(new_s)
                return new_symbols

    def contrast(self, reference_model_pg, hypothetical_model_pg):
        """
        Compute the contrast between the reference model and the hypothetical model.

        Args:
            reference_model_pg: The program graph of the reference model. Tagged with "reference".
            hypothetical_model_pg: The program graph of the hypothetical model. Tagged with "hypothetical".

        Returns:
            A string representing the contrast between the two models.
        """
        ctl = Control(["--warn=none"])
        ctl.add("base", [], reference_model_pg)
        ctl.add("base", [], hypothetical_model_pg)

        with path("asplain.encodings", "contrast.lp") as contrast_encoding:
            log.info("Loading encoding: %s", contrast_encoding)
            ctl.load(str(contrast_encoding))

        ctl.ground([("base", [])])
        contrast_prg = ""
        # Add a custom prune function
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                contrast_prg = "\n".join([str(s) + "." for s in m.symbols(shown=True)])
        return contrast_prg

    def explain(
        self,
        reference_model_symbols: Sequence[Symbol],
        query_include: Sequence[str],
        query_exclude: Sequence[str],
        preference_files: Optional[str] = None,
        model_number: int = 1,
    ):
        """
        Compute the contrastive explanation for the given model and queries.

        Args:
            reference_model_symbols: The program graph of the reference model.
            query_include: The symbols that must be included in the explanation.
            query_exclude: The symbols that must be excluded in the explanation.

        Returns:
            List of programs defining an explanation graph. Graphs are defined using predicates: `edge/2`, `node/1` and `attr/4`
        """
        ctl = Control(["0", "--warn=none"])
        reference_model_pg = self.tag_symbols(reference_model_symbols, "reference")
        reference_model_pg = "\n".join([str(s) + "." for s in reference_model_pg])
        ctl.add("base", [], reference_model_pg)

        q_prg = query_to_pgr(query_include, query_exclude)
        ctl.add("base", [], q_prg)

        # Find hypo
        with path("asplain.encodings", "all_hypo.lp") as base_encoding:
            log.info("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))

        if preference_files is None:
            preference_files = []

        for f in preference_files:
            log.info("Loading encoding: %s", f)
            ctl.load(f)

        ctl.ground([("base", [])])

        hypo_explanations = []
        ctl.configuration.solve.opt_mode = "optN"
        with ctl.solve(yield_=True) as handle:
            for m in handle:

                if not m.optimality_proven:
                    log.debug("Optimality not proven for model, skipping it.")
                    continue
                hypothetical_model_pg = "\n".join([str(s) + "." for s in m.symbols(shown=True)])
                log.info(f"=================Found Hypothetical explanation {m.number}:")
                log.debug(hypothetical_model_pg)
                hypo_explanations.append(hypothetical_model_pg)
                if self._store:
                    hypo_explanation_file = os.path.join(
                        self._output_dir, f"model-{model_number}-hypothetical-{m.number}.lp"
                    )
                    with open(hypo_explanation_file, "w") as f:
                        f.write(hypothetical_model_pg)
                        log.info("Hypothetical explanation saved in " + f.name)
                if self._visualize:
                    self.viz_graph(
                        hypothetical_model_pg,
                        "hypothetical",
                        "Hypothetical Model Program Graph",
                        file_name=f"model-{model_number}-hypothetical-{m.number}",
                        draw_types=["explanation", "model"],
                    )

                hypothetical_model_pg = self.tag_symbols(hypothetical_model_pg, "hypothetical")
                hypothetical_model_pg = "\n".join([str(s) + "." for s in hypothetical_model_pg])
                contrast_prg = self.contrast(reference_model_pg, hypothetical_model_pg)

                if self._store:
                    contrast_file = os.path.join(self._output_dir, f"model-{model_number}-contrast-{m.number}.lp")
                    with open(contrast_file, "w") as f:
                        f.write(contrast_prg)
                        log.info("Contrast saved in " + f.name)

                if self._visualize:
                    self.viz_graph(
                        contrast_prg,
                        "contrast",
                        "Contrastive explanation",
                        file_name=f"model-{model_number}-contrast-{m.number}",
                        draw_types=["contrast", "model"],
                        open=True,
                    )

        if len(hypo_explanations) == 0:
            log.error("No hypothetical explanation found")
            return []

    def viz_reify(self, reified_prg: str) -> None:

        fb = Factbase()
        ctl = Control(["--warn=none"])
        ctx = ClingraphContext()
        ctl.add("base", [], reified_prg)

        with path("asplain.encodings", "viz_reify.lp") as clingraph_encoding:
            ctl.load(str(clingraph_encoding))
        enable_python()
        ctl.ground([("base", [])], context=ctx)
        ctl.solve(on_model=fb.add_model)
        graphs = compute_graphs(fb, graphviz_type="directed")
        files = render(graphs, view=False, directory=self._output_dir, name_format="reify", format="svg")
        for _, f in files.items():
            log.info("Reify: " + f)

    def viz_graph(
        self,
        explanation_graph: str,
        graph_type: str,
        title: str,
        file_name: str = "explanation",
        draw_types: [str] = None,
        open=False,
    ) -> None:
        """
        Visualize the explanation graph using cligraph

        Args:
            explanation_graph: The explanation graph to visualize.
            name: The name of the output file. File will be stored in the same directory
                    as the domain files, inside the `out` directory.
        """
        if not draw_types:
            draw_types = []

        fb = Factbase()
        ctl = Control(["--warn=none"])
        ctx = ClingraphContext()
        ctl.add("base", [], explanation_graph)
        ctl.add("base", [], f'title("{title}").')
        ctl.add("base", [], f"graph_type({graph_type}).")

        for d in draw_types:
            ctl.add("base", [], f"draw_type({d}).")

        with path("asplain.encodings", "viz_pg.lp") as clingraph_encoding:
            ctl.load(str(clingraph_encoding))
        enable_python()
        ctl.ground([("base", [])], context=ctx)
        ctl.solve(on_model=fb.add_model)
        graphs = compute_graphs(fb, graphviz_type="directed")
        files = render(graphs, view=open, directory=self._output_dir, name_format=f"{file_name}", format="svg")
        for _, f in files.items():
            log.info(f"Graph for {graph_type} titled '{title}' saved in: {f}")
