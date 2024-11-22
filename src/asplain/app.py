import sys
from textwrap import dedent
from typing import Any, Callable, Optional, Sequence

from clingo import Application, ApplicationOptions, Control, Flag, Model

from . import Asplain
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
        self._explanation_preference_file: Optional[Sequence[str]] = None

    def parse_log_level(self, log_level: str) -> bool:
        """
        Parse log
        """
        if log_level is not None:
            self._log_level = log_level.upper()
            return self._log_level in ["INFO", "WARNING", "DEBUG", "ERROR"]

        return True

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
            self.parse_general("_explanation_preference_file"),
            argument="<explanation-preference>",
        )
        options.add(
            group,
            "model",
            dedent(
                """\
                A fixed model to explain. Input should be an ASP program using facts.
                            If this parameter is not provided, the solving will follow normally in search for models. """
            ),
            self.parse_general("_model"),
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

    def _divide_query_string(self, query_string: str) -> tuple[list[str], list[str]]:
        """
        Divide the query string into atoms to include and exclude
        """
        include = [atom for atom in query_string.split() if not atom.startswith("-")]
        exclude = [atom[1:] for atom in query_string.split() if atom.startswith("-")]
        return include, exclude

    def on_model(self, model: Model) -> None:
        """
        Print a model on the console. If no query was provided, it asks the user for one
        """
        model_symbols = [str(s) for s in model.symbols(atoms=True, shown=True, theory=True)]
        if self._query:
            query = self._query
        else:
            print(colored("yellow", "Model:" + str(model_symbols)))
            query = input(
                colored(
                    "yellow",
                    "What do you want to explain? Separate atoms by spaces, write -a to force atom a to not appear (Press enter to skip): ",
                )
            )
            if query.lower() == "":
                pass

        include, exclude = self._divide_query_string(query)
        graphs = self._explainer.explain(model_symbols, include, exclude)
        for i, g in enumerate(graphs):
            self._explainer.viz_explanation_graph(g, name=f"model-{model.number}-explanation-{i}")

    def main(self, ctl: Control, files: Sequence[str]) -> None:
        """
        Main function ran on call
        """
        # pylint: disable=W0201
        configure_logging(sys.stderr, self._log_level, sys.stderr.isatty())  # type: ignore
        self._explainer = Asplain(files, [self._explanation_preference_file])  # type: ignore
        if self._model:
            ctl.add("base", [], self._model)
        else:
            for f in files:
                ctl.load(f)

        ctl.ground([("base", [])])
        ctl.solve(on_model=self.on_model)
