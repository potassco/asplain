import os
from importlib.resources import path
from typing import Dict, List, Sequence

from clingexplaid.transformers import RuleIDTransformer
from clingo import Control, Function, Number, Symbol
from clingo.script import enable_python

# pylint: disable=E0401
from clingox.reify import ReifiedTheory, ReifiedTheoryTerm, Reifier
from clingraph.clingo_utils import ClingraphContext  # type: ignore
from clingraph.graphviz import compute_graphs, render  # type: ignore
from clingraph.orm import Factbase  # type: ignore

from ..transformers.graph_transformer import GraphTransformer
from ..utils.logging import get_logger
from .base_explainer import Explainer

log = get_logger("main")


def reify(prg: str = "") -> str:
    """
    Do the reification using clingox Reifier
    """
    symbols: List[Symbol] = []

    ctl = Control(["--warn=none"])
    reifier = Reifier(symbols.append, reify_steps=False)
    ctl.register_observer(reifier)
    ctl.add("base", [], prg)
    ctl.ground([("base", [])])

    theory_symbols: Dict[int, Symbol] = {}

    for k, v in theory_symbols.items():
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

        self._rule_tagged_prg = ""
        transformer = RuleIDTransformer()
        for f in self._domain_files:
            self._rule_tagged_prg += transformer.parse_file(f)

        with open(os.path.join(self._output_dir, "rule_tagged.lp"), "w") as f:
            f.write(self._rule_tagged_prg)

            log.debug("Transformed program: \n%s", self._rule_tagged_prg)
            log.info("Transformed encoding saved in " + f.name)

        # TODO add externals to program to make sure negation is not removed when grounding

        self._reified_prg = reify(self._rule_tagged_prg)
        with open(os.path.join(self._output_dir, "reify.lp"), "w") as f:
            f.write(self._reified_prg)
            log.info("Reified program saved in " + f.name)

    def explain(
        self,
        model_symbols: Sequence[str],
        query_include: Sequence[str],
        query_exclude: Sequence[str],
        prune: bool = False,
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

        log.info("Model: %s", model_symbols)
        log.info(
            "Will explain %s %s",
            ", why  ".join([""] + [str(q) for q in query_include]),
            ", why not".join([""] + [str(q) for q in query_exclude]),
        )
        self.assert_is_model(model_symbols)
        ctl_args = ["0", "--warn=none"]

        ctl = Control(arguments=ctl_args)
        constraint_model_prg = "\n".join([f":- not hold({str(s)})." for s in model_symbols])
        ctl.add("base", [], constraint_model_prg)
        ctl.add("base", [], self._reified_prg)

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

    def viz_explanation_graph(
        self, explanation_graph: str, name: str = "explanation", natural_language_explanation: str = None
    ) -> None:
        """
        Visualize the explanation graph using cligraph

        Args:
            explanation_graph: The explanation graph to visualize.
            name: The name of the output file. File will be stored in the same directory
                    as the domain files, inside the `out` directory.
        """
        fb = Factbase(prefix="v_")
        ctl = Control(["--warn=none"])
        ctx = ClingraphContext()
        ctl.add("base", [], explanation_graph)

        with path("asplain.encodings", "viz_pg.lp") as clingraph_encoding:
            ctl.load(str(clingraph_encoding))
        enable_python()
        ctl.ground([("base", [])], context=ctx)
        ctl.solve(on_model=fb.add_model)
        graphs = compute_graphs(fb, graphviz_type="directed")
        files = render(graphs, view=True, directory=self._output_dir, name_format=name, format="svg")
        for _, f in files.items():
            log.info("Explanation graph saved in: " + f)
