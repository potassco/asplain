"""Module for Asplain application logic."""

import asyncio
import logging
import os
import sys
from textwrap import dedent
from time import time
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union

from clingo import Application, ApplicationOptions, Control, Flag, Model, Symbol, parse_term

from asplain import Foil, construct_program_graph, set_foil_ctl, set_model_subgraphs_ctl
from asplain.pruning.pruners import PruningMethod, prune_explanation_graph
from asplain.utils.clingo import (
    divide_space_string,
    get_query_prg,
    model_symbols,
    symbols_to_prg,
)
from asplain.utils.logging import colored, configure_logging, save_out
from asplain.utils.viz import viz_graph

try:  # nocoverage
    from asplain.llm.models import ModelTag, OpenAIModel
    from asplain.llm.models.google import GoogleModel
    from asplain.llm.templates import ExplainTemplate
    from asplain.llm.utils import parse_llm_json_response

    INSTALLED_LLMS = True
except ImportError:
    INSTALLED_LLMS = False


log = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes, too-many-public-methods
class AsplainApp(Application):
    """Application for reification with extensions."""

    def __init__(
        self, name: str, constants: Optional[dict[str, str]] = None, on_foil: Optional[Callable[[Foil], None]] = None
    ) -> None:
        """Initialize AsplainApp."""
        self.program_name = name
        self._on_foil = on_foil if on_foil is not None else lambda foil: None
        self._log_level = "WARNING"
        self._constants = constants or {}
        self._query_include: List[Symbol] = []
        self._query_exclude: List[Symbol] = []
        self._assumptions: List[Tuple[str, bool]] = []
        self._number_explanations = 1

        self._dynamic_tags: list[str] = []
        self._cost_encoding: list[str] = []
        self._model_symbols: Optional[list[str]] = None

        self._open: Flag = Flag()

        self._pruning_methods: list[PruningMethod] = []
        if INSTALLED_LLMS:
            self._llm_tag: Optional[ModelTag] = None  # nocoverage

        self.statistics: dict[str, Any] = {
            "Program Graph": {},
            "Reference Graph": {},
            "Contrastive Graph": {},
        }

        self._foil: Optional[Foil] = None

    def parse_file(self, attr_name: str, multi: bool = False) -> Callable[[str], bool]:
        """
        Parse file attributes
        """

        def setter(value: Any) -> bool:
            if not os.path.isfile(value):
                raise ValueError(f"File '{value}' does not exist.")  # nocoverage
            if not multi:
                setattr(self, attr_name, value)
            else:
                current_value = getattr(self, attr_name, [])
                if not isinstance(current_value, list):  # nocoverage
                    log.error("Attribute %s is not a list", attr_name)
                    log.error("Setting value to list")
                    current_value = [current_value]
                current_value.append(value)
                setattr(self, attr_name, current_value)
            return True

        return setter

    def parse_log_level(self, log_level: str) -> bool:  # nocoverage
        """
        Parse log
        """
        if log_level is not None:
            self._log_level = log_level.upper()
            return self._log_level in ["INFO", "WARNING", "DEBUG", "ERROR"]

        return True

    def parse_assumptions(self, value: str) -> bool:
        """
        Parse assumptions string
        """

        true_assumptions, false_assumptions = divide_space_string(value)
        self._assumptions = [(str(parse_term(s)), True) for s in true_assumptions]
        self._assumptions += [(str(parse_term(s)), False) for s in false_assumptions]

        return True

    def parse_number_explanations(self, value: str) -> bool:
        """
        Parse number of explanations
        """
        self._number_explanations = int(value)
        return True

    def parse_query(self, value: str) -> bool:
        """
        Parse query string
        """

        true_queries, false_queries = divide_space_string(value)
        self._query_include = [parse_term(s) for s in true_queries]
        self._query_exclude = [parse_term(s) for s in false_queries]

        return True

    def parse_model(self, value: str) -> bool:
        """
        Save the model command line in the object
        """
        self.parse_file("_model_file")(value)
        ctl = Control(["1", "--warn=none"])
        ctl.load(value)
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                self._model_symbols = [str(s) for s in m.symbols(atoms=True)]
                return True

        log.error("No answer set found for the given model file: %s", value)
        return False

    def parse_llm_tag(self, value: str) -> bool:
        """
        Save the LLM tag for prompting in the object
        """
        if INSTALLED_LLMS:
            if value in [str(m) for m in ModelTag.__members__]:
                tag = ModelTag[value]
                self._llm_tag = tag
                return True
        return False

    def parse_pruning(self, value: str) -> bool:
        """
        Save the pruning method in the object
        """
        if value in [str(m) for m in PruningMethod.__members__]:
            method = PruningMethod[value]
            self._pruning_methods.append(method)
            return True
        return False  # nocoverage

    def register_options(self, options: ApplicationOptions) -> None:
        """Register command line options."""
        group = colored("blue", "Asplain Options")

        options.add(
            group,
            "log",
            dedent(
                """\
                Provide logging level.
                            <level> ={DEBUG|INFO|ERROR|WARNING}
                            (default: WARNING)"""
            ),
            self.parse_log_level,
            argument="<level>",
        )
        options.add(
            group,
            "model",
            dedent(
                """\
                File with a fixed model to explain. Input should be an ASP program using facts.
                If this parameter is not provided, the solving will follow normally in search for models. """
            ),
            self.parse_model,
            argument="<model>",
        )

        options.add(
            group,
            "query",
            dedent(
                """\
                A query to explain. Input should be atoms separated by spaces.
                            Negated atoms are preceded by '-'.
                            If not given, queries will be provided interactively via the command line"""
            ),
            self.parse_query,
            argument="<query>",
        )

        options.add(
            group,
            "assumptions",
            dedent(
                """\
                Assumptions to enforce. Input should be atoms separated by spaces.
                            False assumptions are preceded by '-'.
                            If not given, assumptions will be provided interactively via the command line"""
            ),
            self.parse_assumptions,
            argument="<assumptions>",
        )

        options.add(
            group,
            "nexplanations",
            dedent(
                """\
                Number of explanations to compute. (default: 1)"""
            ),
            self.parse_number_explanations,
            argument="<nexplanations>",
        )

        if INSTALLED_LLMS:
            options.add(
                group,
                "llm",
                dedent(
                    f"""\
                    Generate a natural language explanation using an LLM.
                                <llm-tag> ={{{"|".join([str(m) for m in ModelTag.__members__])}}}
                    """
                ),
                self.parse_llm_tag,
                argument="<llm-tag>",
            )

        options.add(
            group,
            "prune,p",
            dedent(
                f"""\
                Apply pruning to the explanation graph to simplify it.
                Multiple pruning methods can be applied by providing this argument multiple self.statistics.
                They will be applied in the order they are given.
                            <method> ={{{"|".join([str(m) for m in PruningMethod.__members__])}}}
                """
            ),
            self.parse_pruning,
            argument="<method>",
            multi=True,
        )

        options.add(
            group,
            "dynamic-tags",
            dedent(
                """\
                Preference file for automatic tagging."""
            ),
            self.parse_file("_dynamic_tags", multi=True),
            argument="<dynamic-tags>",
            multi=True,
        )

        options.add(
            group,
            "cost-encoding",
            dedent(
                """\
                Encoding defining the cost function to calculate the best foils via optimization."""
            ),
            self.parse_file("_cost_encoding", multi=True),
            argument="<cost-encoding>",
            multi=True,
        )

        options.add_flag(
            group,
            "open",
            dedent(
                """\
                If active the graphs for all contrastive explanations will be opened automatically."""
            ),
            self._open,
        )

    def size_for_statistics(self, name: str, pg: str) -> dict[str, Any]:
        """
        Compute size statistics for a program graph.
        """
        ctl = Control(["--warn=none"])
        ctl.add("base", [], pg)
        ctl.load(str(os.path.dirname(__file__)) + "/utils/node-count.lp")
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as hnd:
            for m in hnd:
                for s in m.symbols(shown=True):
                    if s.name == "number" and len(s.arguments) == 2:
                        category = str(s.arguments[0])
                        count = s.arguments[1].number
                        self.statistics[name][category] = count

        return self.statistics[name]  # type: ignore

    def on_statistics(self, _: Any, accu: dict[str, Any]) -> None:
        """
        Callback to collect statistics after solving
        """
        self.statistics["Cost encoding"] = {"count": len(self._cost_encoding)}
        self.statistics["Pruning methods"] = {"count": len(self._pruning_methods)}
        self.statistics["Explanations"] = {"count": self._number_explanations}
        self.statistics["Number of changes"] = (
            {"added": len(self._foil.added_rules), "removed": len(self._foil.removed_rules)}
            if self._foil is not None
            else {"added": -1, "removed": -1}
        )
        accu["Asplain"] = self.statistics

    def print_model(self, model: Model, _) -> None:  # type: ignore
        """Print the model's symbols."""
        symbols = model.symbols(shown=True)
        print(" ".join([str(s) for s in model_symbols(symbols)]))

    def main(self, control: Control, files: Sequence[str]) -> None:
        """
        Main entry point.
        """
        # pylint: disable=W0201
        # pylint: disable=too-many-branches, too-many-statements

        configure_logging(sys.stderr, self._log_level, sys.stderr.isatty())  # type: ignore
        query_prg = get_query_prg(self._query_include, self._query_exclude)
        cost_prg = ""
        if self._cost_encoding:
            for cost_file in self._cost_encoding:
                log.info("Loading cost encoding file: %s", cost_file)
                with open(cost_file, "r", encoding="utf-8") as cf:
                    cost_prg += cf.read() + "\n"

        start_time = time()
        reference_pg = construct_program_graph(
            list(files),
            constants=self._constants,
            assumptions=self._assumptions,
            dynamic_tags_files=self._dynamic_tags,
        )
        self.statistics["Program Graph"]["time"] = round(time() - start_time, 2)
        save_out("reference_pg.lp", reference_pg)
        viz_graph(
            pg=reference_pg,
            title="Program Graph",
            name="reference_pg",
        )
        self.size_for_statistics("Program Graph", reference_pg)
        start_time = time()
        model_subgraphs_ctl = set_model_subgraphs_ctl(pg=reference_pg, ctl=control, model_symbols=self._model_symbols)
        with model_subgraphs_ctl.solve(yield_=True, on_statistics=self.on_statistics) as hnd:  # type: ignore
            model_found = False
            for model in hnd:
                model_found = True
                symbols = model.symbols(shown=True)
                reference_model_pg = symbols_to_prg(symbols)
                self.statistics["Reference Graph"]["time"] = round(time() - start_time, 2)
                save_out(f"reference_model_{model.number}.lp", reference_model_pg)
                viz_graph(
                    pg=reference_model_pg,
                    title="Reference Graph",
                    name=f"reference_model_pg_{model.number}",
                )
                start_time = time()
                foil_ctl = set_foil_ctl(
                    pg=reference_model_pg,
                    query_prg=query_prg,
                    cost_prg=cost_prg,
                    number_of_foils=self._number_explanations,
                )
                with foil_ctl.solve(yield_=True) as foil_hnd:
                    foil_found = False
                    for foil_model in foil_hnd:
                        if not foil_model.optimality_proven:
                            log.info("Skipping non-optimal foil model %s", foil_model.number)
                            continue
                        foil_found = True
                        self.statistics["Contrastive Graph"]["time"] = round(time() - start_time, 2)

                        start_time = time()
                        explanation_symbols = list(foil_model.symbols(shown=True))
                        for method in self._pruning_methods:
                            log.info("Applying pruning method %s to foil model", method)
                            explanation_symbols = prune_explanation_graph(
                                explanation_symbols,
                                method=method,
                            )
                        self.statistics["Contrastive Graph"]["pruning_time"] = round(time() - start_time, 2)
                        self.size_for_statistics("Contrastive Graph", symbols_to_prg(explanation_symbols))

                        explanation_graph = symbols_to_prg(explanation_symbols)
                        log.debug("Saving contrastive explanation...")
                        save_out(
                            f"contrastive_pg_{model.number}_{foil_model.number}.lp",
                            explanation_graph,
                        )
                        log.debug("Inspecting foil...")
                        self._foil = Foil.from_explanation_graph(explanation_graph)
                        self._on_foil(self._foil)
                        self._foil.print()

                        viz_graph(
                            pg=explanation_graph,
                            title="Contrastive Graph",
                            name=f"contrastive_pg_{model.number}_{foil_model.number}",
                            show=self._open.flag,
                        )
                        if INSTALLED_LLMS:  # nocoverage
                            if self._llm_tag is not None:
                                # Prompt the LLM
                                if self._llm_tag.value.openai is not None:
                                    log.info("Using OpenAI API")
                                    llm: Union[OpenAIModel, GoogleModel] = OpenAIModel(model_tag=self._llm_tag)
                                elif self._llm_tag.value.google is not None:
                                    log.info("Using Google API")
                                    llm = GoogleModel(model_tag=self._llm_tag)
                                else:
                                    raise ValueError(f"LLM tag {self._llm_tag} is not supported.")
                                template = ExplainTemplate(contrastive_program_graph=explanation_graph)
                                print("LLM Explanation:")
                                response = asyncio.run(llm.prompt_template(template))
                                response_message = parse_llm_json_response(response)
                                print(colored("grey", response_message))
                    if not foil_found:
                        log.warning("No foil found.")

            if not model_found:
                log.warning("UNSATISFIABLE. Will proceed to explain.")
                foil_ctl = set_foil_ctl(
                    pg=reference_pg,
                    number_of_foils=self._number_explanations,
                    query_prg=query_prg,
                    cost_prg=cost_prg,
                )
                with foil_ctl.solve(yield_=True) as foil_hnd:
                    foil_found = False
                    for foil_model in foil_hnd:
                        if not foil_model.optimality_proven:
                            log.info("Skipping non-optimal foil model %s", foil_model.number)
                            continue
                        foil_found = True
                        explanation_graph = symbols_to_prg(list(foil_model.symbols(shown=True)))
                        save_out(
                            f"contrastive_pg_UNSAT_{foil_model.number}.lp",
                            explanation_graph,
                        )
                        viz_graph(
                            pg=explanation_graph,
                            title="Contrastive Graph",
                            name=f"contrastive_pg_UNSAT_{foil_model.number}",
                            show=self._open.flag,
                        )
                        explanation_symbols = list(foil_model.symbols(shown=True))
                        for method in self._pruning_methods:
                            log.info("Applying pruning method %s to foil model", method)
                            explanation_symbols = prune_explanation_graph(
                                explanation_symbols,
                                method=method,
                            )
                        explanation_graph = symbols_to_prg(explanation_symbols)

                        self._foil = Foil.from_explanation_graph(explanation_graph)
                        self._on_foil(self._foil)
                        self._foil.print()
                    if not foil_found:
                        log.warning("No foil found.")
