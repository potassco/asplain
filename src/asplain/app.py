import os
import sys
from textwrap import dedent
from typing import Any, Callable, Optional, Sequence

from clingo import Application, ApplicationOptions, Control, Flag, Model

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
        self._model = None
        self._query = None
        self._explanation_preference: Optional[Sequence[str]] = []
        self._predicates_file: Optional[Sequence[str]] = None
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
            self.parse_file("_model"),
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
            self.parse_general("_query"),
            argument="<query>",
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

    def _divide_query_string(self, query_string: str) -> tuple[list[str], list[str]]:
        """
        Divide the query string into atoms to include and exclude
        """
        include = [atom for atom in query_string.split() if not atom.startswith("-")]
        exclude = [atom[1:] for atom in query_string.split() if atom.startswith("-")]
        return include, exclude

    def print_model(self, model: Model, printer: Callable[[], None]) -> None:
        """
        Print a model on the console. If no query was provided, it asks the user for one
        """
        for sym in model.symbols(shown=True):
            sys.stdout.write(f"{sym} ")
        sys.stdout.write("\n")

        # -------- Interactive query --------
        if self._query:
            query = self._query
        else:
            query = input(
                colored(
                    "yellow",
                    dedent(
                        """
                    What do you want to explain?
                    Provide the atoms you would like in your model separated by spaces.
                    Write -a to force atom a to not appear. (Press enter to skip): """,
                    ),
                )
            )
            if query.lower() == "":
                print("pass")
                return

        # -------- Explain with Contrastive --------
        include, exclude = self._divide_query_string(query)
        model_symbols = [str(s) for s in model.symbols(atoms=True, shown=True, theory=True)]
        graphs = self._explainer.explain(model_symbols, include, exclude, prune=self._prune)

        for i, g in enumerate(graphs):
            log.info("--------------------Explanation %d\n%s", i, g)

            # -------- Explain with LLM --------
            llm_response = None
            if self._use_llm:
                predicates = ""
                if self._predicates_file:
                    with open(self._predicates_file, "r") as f:
                        predicates = " ".join(f.readlines())

                if self._model_tag == "openai":
                    # OPEN AI
                    llm_model = OpenAIModel(ModelTag.GPT_4O_MINI)
                elif self._model_tag == "deepseek":
                    # DEEPSEEK
                    llm_model = OllamaModel(ModelTag.DEEPSEEK_R1_14B)
                elif self._model_tag == "llama":
                    # DEFAULT LLAMA
                    llm_model = OllamaModel(ModelTag.LLAMA_3_2_1B)
                else:
                    raise ValueError(f"Model tag invalid: {self._model_tag}")

                prompt_template = ExplainLargeTemplate(
                    graph=g,
                    predicates=predicates,
                )
                llm_response = llm_model.prompt_template(prompt_template)
                print_llm_message(llm_response)

            # -------- Visualize Explanation --------
            self._explainer.viz_explanation_graph(
                g,
                name=f"{{graph_name}}-model-{model.number}-explanation-{i}",
                natural_language_explanation=llm_response,
            )

    def main(self, ctl: Control, files: Sequence[str]) -> None:
        """
        Main function ran on call
        """
        # pylint: disable=W0201
        configure_logging(sys.stderr, self._log_level, sys.stderr.isatty())  # type: ignore
        self._explainer = ContrastiveExplainer(files, self._explanation_preference)  # type: ignore
        if self._model:
            ctl.load(self._model)
        else:
            for f in files:
                ctl.load(f)

        ctl.ground([("base", [])])
        ctl.solve()
