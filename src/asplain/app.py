import os
import sys
from textwrap import dedent
from typing import Any, Callable, Optional, Sequence

from clingo import Application, ApplicationOptions, Control, Flag, Model, parse_term

from .explainers import ContrastiveExplainer
from .llm.models import ModelTag, OllamaModel
from .llm.models.openai import OpenAIModel
from .llm.templates import ExplainLargeTemplate
from .llm.utils import print_llm_message
from .utils.logging import colored, configure_logging, get_logger

log = get_logger("main")


class AsplainApp(Application):

    def __init__(self, name: str):
        """
        Create application
        """
        self.program_name = name
        self._log_level = "WARNING"
        self._model_symbols = None
        self._query_include = []
        self._query_exclude = []
        self._assumptions = []
        self._explanation_preference: Optional[Sequence[str]] = []
        # self._predicates_file: Optional[Sequence[str]] = None
        self._model_tag = "openai"
        self._use_llm: Flag = Flag()
        self._prune: Flag = Flag()

    def parse_log_level(self, log_level: str) -> bool:
        """
        Parse log
        """
        if log_level is not None:
            self._log_level = log_level.upper()
            return self._log_level in ["INFO", "WARNING", "DEBUG", "ERROR"]

        return True

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
                self.__setattr__(attr_name, current_value)
            return True

        return setter

    def parse_assumptions(self, value) -> bool:
        """
        Parse assumptions string
        """

        true_assumptions, false_assumptions = self._divide_space_string(value)
        self._assumptions = [(parse_term(s), True) for s in true_assumptions]
        self._assumptions += [(parse_term(s), False) for s in false_assumptions]

        return True

    def parse_query(self, value) -> bool:
        """
        Parse query string
        """

        true_queries, false_queries = self._divide_space_string(value)
        self._query_include = [parse_term(s) for s in true_queries]
        self._query_exclude = [parse_term(s) for s in false_queries]

        return True

    def parse_model(self, value: str) -> bool:
        self.parse_file("_model_file")(value)
        ctl = Control(["1", "--warn=none"])
        ctl.load(value)
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                self._model_symbols = m.symbols(atoms=True)
                return True

        log.error("No answer set found for the given model file: %s", value)
        return False

    def parse_general(self, attr_name: str) -> Callable[[str], bool]:
        """
        Parse general attributes
        """

        def setter(value: Any) -> bool:
            self.__setattr__(attr_name, value)
            return True

        return setter

    def register_options(self, options: ApplicationOptions) -> None:
        """
        Add custom options
        """
        group = colored("red", "Asplain Options")

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
            "explanation-preference",
            dedent(
                """\
                Preference file for explanations."""
            ),
            self.parse_file("_explanation_preference", multi=True),
            argument="<explanation-preference>",
            multi=True,
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

        options.add_flag(
            group,
            "prune",
            dedent(
                """\
                If active responds the pruned graph, where only nodes and edges connected to the query are shown.
                """
            ),
            self._prune,
        )

        options.add_flag(
            group,
            "llm",
            dedent(
                """\
                If active provides the user with an llm chat for explaining the query.
                """
            ),
            self._use_llm,
        )
        options.add(
            group,
            "model-tag",
            dedent(
                """\
                Specifies which LLM model is used if the llm feature is active.
                """
            ),
            self.parse_general("_model_tag"),
            argument="<model-tag>",
        )

        options.add(
            group,
            "predicates",
            dedent(
                """\
                Text explaning meaning of predicates."""
            ),
            self.parse_file("_predicates_file"),
            argument="<predicates>",
        )

    @staticmethod
    def _divide_space_string(space_string: str) -> tuple[list[str], list[str]]:
        """
        Divide the string into atoms to include and exclude
        """
        include = [atom for atom in space_string.split() if not atom.startswith("-")]
        exclude = [atom[1:] for atom in space_string.split() if atom.startswith("-")]
        return include, exclude

    def print_model(self, model: Model, printer: Callable[[], None]) -> None:
        """
        Print a model on the console. If no query was provided, it asks the user for one
        """
        # log.info("Model: %s", model)
        output = ""
        failed_query = False
        model_pg = "\n".join([str(s) + "." for s in model.symbols(shown=True)])
        for sym in model.symbols(shown=True):
            # print(sym.arguments[0].name)
            if sym.name == "node_tag" and str(sym.arguments[1]) == "true" and sym.arguments[0].name == "atom":
                output += str(sym.arguments[0].arguments[0]) + " "
            if sym.name == "fail_query":
                failed_query = True

        color = "red" if failed_query else "green"
        output = colored(color, output)
        if failed_query:
            output += "\n" + colored("red", "(Query failed to hold in the model)")
        else:
            output += "\n" + colored("green", "(Query holds in the model)")
        sys.stdout.write(output + "\n")

        self._explainer.viz_graph(
            model_pg, "reference", "Model Program Graph", file_name=f"model-{model.number}", draw_types=["model"]
        )
        reference_explanation_file = os.path.join(self._explainer._output_dir, f"model-{model.number}.lp")
        with open(reference_explanation_file, "w") as f:
            f.write(model_pg)
            log.info("Reference model saved in " + f.name)

        self._explainer.explain(
            model_pg, self._query_include, self._query_exclude, self._explanation_preference, model.number
        )

    def main(self, ctl: Control, files: Sequence[str]) -> None:
        """
        Main function ran on call
        """
        # pylint: disable=W0201
        configure_logging(sys.stderr, self._log_level, sys.stderr.isatty())  # type: ignore
        log.info("Model: %s", self._model_symbols)
        log.info(
            "Will explain %s %s",
            ", why  ".join([""] + [str(q) for q in self._query_include]),
            ", why not".join([""] + [str(q) for q in self._query_exclude]),
        )
        # Set the assumptions
        output_dir = os.path.join(os.path.dirname(files[0]), "out")
        self._explainer = ContrastiveExplainer(output_dir, True, True)  # type: ignore
        pg = self._explainer.generate_pg(files, self._assumptions)
        if pg is None:
            log.error("No program graph generated. Exiting.")
            return

        self._explainer.setup_ctl_from_pg(ctl, pg, self._model_symbols, self._query_include, self._query_exclude)

        ctl.ground([("base", [])])
        result = ctl.solve()
        if not result.satisfiable:
            log.warning("------ UNSATISFIABLE ------")
            log.warning("Calculating contrastive explanation without a query for the pg without a model")
            self._explainer.explain(pg, [], [], self._explanation_preference, 0)
