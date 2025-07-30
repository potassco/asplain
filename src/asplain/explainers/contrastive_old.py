import os
from importlib.resources import path
from typing import Callable, Dict, List, Sequence, Tuple

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
    print("Visiting terms in theory")
    for atm in thy:
        for elem in atm.elements:
            for term in elem.terms:
                cb(term)
        cb(atm.term)
        guard = atm.guard
        if guard:
            cb(guard[1])


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
    log.info("Reifying program")
    symbols: List[Symbol] = []

    ctl = Control(["--warn=none"])
    reifier = Reifier(symbols.append, reify_steps=False)
    ctl.register_observer(reifier)
    ctl.add("base", [], prg)
    if files is not None:
        for f in files:
            ctl.load(f)

    ctl.ground([("base", [])])

    theory_symbols: Dict[int, Symbol] = {}
    _visit_terms(ReifiedTheory(symbols), lambda term: _term_symbols(term, theory_symbols))

    for k, v in theory_symbols.items():
        print(f"Reified theory symbol: {k} -> {v}")
        symbols.append(Function("theory_symbol", [Number(k), v]))
    return "\n".join([f"{str(s)}." for s in symbols])


class ContrastiveExplainer(Explainer):
    """
    Explanation class for contrastive explanations.
    """

    def __init__(self, domain_files: Sequence[str], explanation_preference_files: Sequence[str]):
        """
        Create an Asplain instance.

        Args:
            domain_files: List of ASP files containing the domain knowledge.
            explanation_preference_files: List of ASP files containing the explanation preferences (abducibles, distance).
        """
        self._domain_files = domain_files
        self._explanation_preference_files = explanation_preference_files

        # Output directory for intermediate files and images
        domain_base_path = os.path.dirname(self._domain_files[0])
        self._output_dir = os.path.join(domain_base_path, "out")
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)

    def reify(self, assumptions: Sequence[Tuple[Symbol, bool]]) -> None:
        """ """

        assumptions_as_constraints = "\n\n%%%%%%%%%%%% Assumptions as constraints %%%%%%%%%%%%\n"
        assumptions_as_constraints += "\n".join([f":- not {str(s)}." for s, b in assumptions if b])
        assumptions_as_constraints += "\n".join([f":- {str(s)}." for s, b in assumptions if not b])

        self._reified_prg = reify(assumptions_as_constraints, self._domain_files)
        with open(os.path.join(self._output_dir, "reify.lp"), "w") as f:
            f.write(self._reified_prg)
            log.info("Reified program saved in " + f.name)
        # self.viz_reify()

    def compute_pg(
        self,
    ):
        ctl_args = ["1", "--warn=none"]
        ctl = Control(arguments=ctl_args)
        ctl.add("base", [], self._reified_prg)
        with path("asplain.encodings", "reify_to_pg.lp") as base_encoding:
            log.info("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))

        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                self._pg = "\n".join([str(s) + "." for s in m.symbols(shown=True)])
        if not self._pg:
            log.error("No program graph found")
            return

        with open(os.path.join(self._output_dir, "pg.lp"), "w") as f:
            f.write(self._pg)
            log.info("Program graph saved in " + f.name)

        extra_prg = """
        node(N,reference) :- node(N).
        edge(N,reference) :- edge(N).
        edge_attr(N,T,V,reference) :- edge(N,T,V).
        """
        self.viz_explanation_graph(self._pg + extra_prg, name="pg", draw=["reference"], draw_types=["pg"])

    def explain(
        self,
        model_symbols: Sequence[str],
        query_include: Sequence[str],
        query_exclude: Sequence[str],
        assumptions: Sequence[Tuple[Symbol, bool]],
    ) -> Sequence[str]:
        """
        Explain the given model and queries.

        Args:
            model_symbols: The symbols of the model to explain.
            query_include: The symbols that must be included in the explanation.
            query_exclude: The symbols that must be excluded in the explanation.

        Returns:
            List programs defining an explanation graph. Graphs are defined using predicates: `edge/2`, `node/1` and `attr/4`
        """

        self.reify(assumptions)
        self.compute_pg()
        # return True
        log.info("Model: %s", model_symbols)
        log.info(
            "Will explain %s %s",
            ", why  ".join([""] + [str(q) for q in query_include]),
            ", why not".join([""] + [str(q) for q in query_exclude]),
        )
        # if assumptions is None:
        #     assumptions = []
        # log.info("Assumptions: %s", [(str(s), b) for s, b in assumptions])
        # self.assert_is_model(model_symbols, assumptions)

        ctl_args = ["1", "--warn=none"]
        ctl = Control(arguments=ctl_args)
        constraint_model_prg = "\n".join([f":- not hold({str(s)})." for s in model_symbols])
        ctl.add("base", [], constraint_model_prg)
        ctl.add("base", [], self._pg)

        with path("asplain.encodings", "all_reference.lp") as base_encoding:
            log.info("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))

        # model_prg = "".join([f"_model(real,{s})." for s in model_symbols])
        # ctl.add("base", [], model_prg)

        ctl.ground([("base", [])])
        reference_explanations = []
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                explanation_graph_prg = "\n".join([str(s) + "." for s in m.symbols(shown=True)])
                reference_explanations.append(explanation_graph_prg)

        if len(reference_explanations) == 0:
            log.warning("No reference explanation found")
        else:
            log.debug("=================\nReference explanation:")
            log.debug(reference_explanations[0])

        ref_prg = reference_explanations[0]
        ctl = Control(arguments=ctl_args)
        ctl.add("base", [], ref_prg)

        qi = "".join([f"_query(include,{s})." for s in query_include])
        ctl.add("base", [], qi)
        qe = "".join([f"_query(exclude,{s})." for s in query_exclude])
        ctl.add("base", [], qe)

        for f in self._explanation_preference_files:
            log.info("Loading encoding: %s", f)
            ctl.load(f)

        with path("asplain.encodings", "all_hypo.lp") as base_encoding:
            log.debug("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))

        ctl.ground([("base", [])])
        contrastive_explanations = []
        ctl.configuration.solve.opt_mode = "optN"
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                if not m.optimality_proven:
                    log.debug("No optimality proven")
                    log.debug(m.cost)
                    continue
                explanation_graph_prg = "\n".join([str(s) + "." for s in m.symbols(shown=True)])
                log.debug("=================\nHypo explanation:")
                log.debug(m.cost)
                log.debug(explanation_graph_prg)
                explanation_graph_prg += ref_prg
                contrastive_explanations.append(explanation_graph_prg)

        if len(contrastive_explanations) == 0:
            log.error("No hypothetical explanation found")

        return contrastive_explanations

    def viz_reify(self) -> None:

        fb = Factbase()
        ctl = Control(["--warn=none"])
        ctx = ClingraphContext()
        ctl.add("base", [], self._reified_prg)

        with path("asplain.encodings", "viz_reify.lp") as clingraph_encoding:
            ctl.load(str(clingraph_encoding))
        enable_python()
        ctl.ground([("base", [])], context=ctx)
        ctl.solve(on_model=fb.add_model)
        graphs = compute_graphs(fb, graphviz_type="directed")
        files = render(graphs, view=True, directory=self._output_dir, name_format="reify", format="svg")
        for _, f in files.items():
            log.info("Reify: " + f)

    def viz_explanation_graph(
        self,
        explanation_graph: str,
        name: str = "explanation",
        natural_language_explanation: str = None,
        draw_types: [str] = None,
        draw: [str] = None,
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
        if not draw:
            draw = []

        fb = Factbase(prefix="v_")
        ctl = Control(["--warn=none"])
        ctx = ClingraphContext()
        ctl.add("base", [], explanation_graph)

        for d in draw_types:
            ctl.add("base", [], f"draw_type({d}).")
        for d in draw:
            ctl.add("base", [], f"draw({d}).")

        with path("asplain.encodings", "viz_pg.lp") as clingraph_encoding:
            ctl.load(str(clingraph_encoding))
        enable_python()
        ctl.ground([("base", [])], context=ctx)
        ctl.solve(on_model=fb.add_model)
        graphs = compute_graphs(fb, graphviz_type="directed")
        files = render(graphs, view=True, directory=self._output_dir, name_format=name, format="svg")
        for _, f in files.items():
            log.info("Explanation graph saved in: " + f)
