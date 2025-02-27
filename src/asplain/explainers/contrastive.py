import os
from importlib.resources import path
from typing import Sequence

from clingo import Control
from clingo.script import enable_python
from clingraph.clingo_utils import ClingraphContext  # type: ignore
from clingraph.graphviz import compute_graphs, render  # type: ignore
from clingraph.orm import Factbase  # type: ignore

from ..transformers.graph_transformer import GraphTransformer
from ..transformers.transformer_pipeline import AbductionPipeline, ModelSupportPipeline
from ..utils.logging import get_logger
from .base_explainer import Explainer

log = get_logger("main")


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

        self._abduction_prg = AbductionPipeline().parse_files(self._domain_files)
        with open(os.path.join(self._output_dir, "abduction.lp"), "w") as f:
            f.write(self._abduction_prg)
            log.info("Abduction encoding saved in " + f.name)

        self._support_prg = ModelSupportPipeline().parse_files(self._domain_files)
        with open(os.path.join(self._output_dir, "support.lp"), "w") as f:
            f.write(self._support_prg)
            log.info("Support encoding saved in " + f.name)

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
        self.assert_is_model(model_symbols)
        ctl_args = ["0", "--opt-mode=optN", "--warn=none", "--project=show"]

        prune_prg = "true" if prune else "false"
        ctl_args.append("-c")
        ctl_args.append(f"reachable={prune_prg}")

        ctl = Control(ctl_args)
        ctl.add("base", [], self._abduction_prg)
        ctl.add("base", [], self._support_prg)
        for f in self._explanation_preference_files:
            ctl.load(f)
        with path("asplain.encodings", "base.lp") as base_encoding:
            ctl.load(str(base_encoding))

        model_prg = "".join([f"_model(real,{s})." for s in model_symbols])
        ctl.add("base", [], model_prg)
        qi = "".join([f"_query(include,{s})." for s in query_include])
        ctl.add("base", [], qi)

        qe = "".join([f"_query(exclude,{s})." for s in query_exclude])
        ctl.add("base", [], qe)

        log.info("Explaining query: %s %s", qi, qe)

        ctl.ground([("base", [])])
        contrastive_explanations = []
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                if not m.optimality_proven:
                    log.debug("Skipped non-optimal model")
                    continue
                explanation_graph_prg = "\n".join([str(s) + "." for s in m.symbols(shown=True)])
                explanation_graph_prg = GraphTransformer().parse_string(explanation_graph_prg)
                log.info(
                    "------ Abducible atoms\n%s",
                    "\n".join(
                        [str(s) for s in m.symbols(atoms=True) if s.name == "_abducible" and len(s.arguments) == 2]
                    ),
                )
                log.info(
                    "------ Abduced atoms \n%s",
                    "\n".join(
                        [str(s) for s in m.symbols(atoms=True) if s.name == "_abduced" and len(s.arguments) == 2]
                    ),
                )

                log.debug("----- Full Explanation \n%s", m.symbols(atoms=True))
                contrastive_explanations.append(explanation_graph_prg)
                # break

        if len(contrastive_explanations) == 0:
            log.warning("No explanation found")
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

        fb = Factbase(default_graph="trace", prefix="viz_")
        ctl = Control(["--warn=none"])
        ctx = ClingraphContext()
        ctl.add("base", [], explanation_graph)
        if natural_language_explanation:
            natural_language_explanation = natural_language_explanation.replace('"', "")
            prg = f"""
            viz_attr(graph,explanation,label,"{natural_language_explanation}").
            """
            ctl.add("base", [], prg)
        with path("asplain.encodings", "clingraph.lp") as clingraph_encoding:
            ctl.load(str(clingraph_encoding))
        enable_python()
        ctl.ground([("base", [])], context=ctx)
        ctl.solve(on_model=fb.add_model)
        graphs = compute_graphs(fb, graphviz_type="directed")
        files = render(graphs, view=True, directory=self._output_dir, name_format=name, format="svg")
        for _, f in files.items():
            log.info("Explanation graph saved in: " + f)
