"""Module for Asplain application logic."""

import asyncio
import logging
import os
import sys
from textwrap import dedent
from time import time
from typing import Any, Callable, Optional, Sequence

from clingo import Application, ApplicationOptions, Control, Flag, Model, parse_term

from asplain import (
    construct_program_graph,
    set_foil_ctl,
    set_model_subgraphs_ctl,
)
from asplain.pruning.pruners import PruningMethod, prune_explanation_graph
from asplain.utils.clingo import (
    divide_space_string,
    foil_inspection,
    get_query_prg,
    model_symbols,
    print_foil,
    symbols_to_prg,
)
from asplain.utils.logging import colored, configure_logging, save_out
from asplain.utils.viz import viz_graph

# from asplain.utils.viz import viz_graph_mock as viz_graph

try:
    from asplain.llm.models import ModelTag, OpenAIModel
    from asplain.llm.models.google import GoogleModel
    from asplain.llm.templates import ExplainTemplate
    from asplain.llm.utils import parse_llm_json_response

    INSTALLED_LLMS = True
except ImportError:
    INSTALLED_LLMS = False


log = logging.getLogger(__name__)


class AsplainApp(Application):
    """Application for reification with extensions."""

    def __init__(self, name, constants: Optional[dict[str, str]] = None) -> None:
        """Initialize AsplainApp."""
        self.program_name = name
        self._log_level = "WARNING"
        self._constants = constants or {}
        self._query_include = []
        self._query_exclude = []
        self._assumptions = []
        self._number_explanations = 1

        self._dynamic_tags = []
        self._cost_encoding = []
        self._model_symbols = None

        self._open: Flag = Flag()

        self._pruning_methods: list[PruningMethod] = []
        if INSTALLED_LLMS:
            self._llm_tag: Optional[ModelTag] = None

        self.statistics = {
            "Program Graph": {},
            "Reference Graph": {},
            "Contrastive Graph": {},
        }

    def parse_file(self, attr_name: str, multi: bool = False) -> Callable[[str], bool]:
        """
        Parse file attributes
        """

        def setter(value: Any) -> bool:
            if not os.path.isfile(value):
                raise ValueError(f"File '{value}' does not exist.")
            if not multi:
                self.__setattr__(attr_name, value)
            else:
                current_value = getattr(self, attr_name, [])
                if not isinstance(current_value, list):
                    log.error("Attribute %s is not a list", attr_name)
                    log.error("Setting value to list")
                    current_value = [current_value]
                current_value.append(value)
                self.__setattr__(attr_name, current_value)  # Use direct assignment instead of __setattr__
            return True

        return setter

    def parse_log_level(self, log_level: str) -> bool:
        """
        Parse log
        """
        if log_level is not None:
            self._log_level = log_level.upper()
            return self._log_level in ["INFO", "WARNING", "DEBUG", "ERROR"]

        return True

    def parse_assumptions(self, value) -> bool:
        """
        Parse assumptions string
        """

        true_assumptions, false_assumptions = divide_space_string(value)
        self._assumptions = [(str(parse_term(s)), True) for s in true_assumptions]
        self._assumptions += [(str(parse_term(s)), False) for s in false_assumptions]

        return True

    def parse_number_explanations(self, value) -> bool:
        """
        Parse number of explanations
        """
        self._number_explanations = int(value)
        return True

    def parse_query(self, value) -> bool:
        """
        Parse query string
        """

        true_queries, false_queries = divide_space_string(value)
        self._query_include = [str(parse_term(s)) for s in true_queries]
        self._query_exclude = [str(parse_term(s)) for s in false_queries]

        return True

    def parse_model(self, value: str) -> bool:
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
        if INSTALLED_LLMS:
            if value in [str(m) for m in ModelTag.__members__]:
                tag = ModelTag[value]
                self._llm_tag = tag
                return True
        return False

    def parse_pruning(self, value: str) -> bool:
        if value in [str(m) for m in PruningMethod.__members__]:
            method = PruningMethod[value]
            self._pruning_methods.append(method)
            return True
        return False

    def register_options(self, options: ApplicationOptions) -> None:
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

    def size_for_statistics(self, name: str, pg: str) -> dict[str, int]:
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

    def on_statistics(self, step, accu) -> None:
        self.statistics["Cost encoding"] = len(self._cost_encoding)
        self.statistics["Pruning methods"] = len(self._pruning_methods)
        self.statistics["Explanations"] = self._number_explanations
        self.statistics["Number of changes"] = (
            {"added": len(self._foil_inspection[1]), "removed": len(self._foil_inspection[2])}
            if self._foil_inspection
            else None
        )
        accu["Asplain"] = self.statistics

    def print_model(self, model: Model, _) -> None:
        symbols = model.symbols(shown=True)
        print(" ".join([str(s) for s in model_symbols(symbols)]))

    def main(self, ctl: Control, files: Sequence[str]) -> None:
        """
        Main entry point.
        """
        # pylint: disable=W0201

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
        model_subgraphs_ctl = set_model_subgraphs_ctl(pg=reference_pg, ctl=ctl, model_symbols=self._model_symbols)
        with model_subgraphs_ctl.solve(yield_=True, on_statistics=self.on_statistics) as hnd:
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
                        self._foil_inspection = foil_inspection(explanation_graph)
                        print_foil(*self._foil_inspection)

                        viz_graph(
                            pg=explanation_graph,
                            title="Contrastive Graph",
                            name=f"contrastive_pg_{model.number}_{foil_model.number}",
                            open=self._open.flag,
                        )
                        if INSTALLED_LLMS:
                            if self._llm_tag is not None:
                                # Prompt the LLM
                                if self._llm_tag.value.openai is not None:
                                    log.info("Using OpenAI API")
                                    llm = OpenAIModel(model_tag=self._llm_tag)
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
                            open=self._open.flag,
                        )
                        explanation_symbols = list(foil_model.symbols(shown=True))
                        for method in self._pruning_methods:
                            log.info("Applying pruning method %s to foil model", method)
                            explanation_symbols = prune_explanation_graph(
                                explanation_symbols,
                                method=method,
                            )
                        explanation_graph = symbols_to_prg(explanation_symbols)

                        self._foil_inspection = foil_inspection(explanation_graph)
                        print_foil(*self._foil_inspection)
                    if not foil_found:
                        log.warning("No foil found.")
