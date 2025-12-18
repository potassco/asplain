"""Module for Asplain application logic."""

import logging
import os
import sys
from textwrap import dedent
from typing import Any, Callable, Optional, Sequence

from clingo import Application, ApplicationOptions, Control, Model, parse_term

from asplain import construct_contrastive, construct_program_graph, set_foil_ctl, set_model_subgraphs_ctl
from asplain.utils.clingo import divide_space_string, get_query_prg, model_symbols, print_foil, symbols_to_prg
from asplain.utils.logging import colored, configure_logging, save_out
from asplain.utils.viz import viz_graph

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
        self._model_symbols = None

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
        distance_prg = ""  # TODO Get from command line

        reference_pg = construct_program_graph(
            list(files),
            constants=self._constants,
            assumptions=self._assumptions,
            dynamic_tags_files=self._dynamic_tags,
        )
        save_out("reference_pg.lp", reference_pg)
        viz_graph(
            pg=reference_pg,
            graphs=["reference"],
            title="Reference Graph",
            name="reference_pg",
        )
        model_subgraphs_ctl = set_model_subgraphs_ctl(pg=reference_pg, ctl=ctl, model_symbols=self._model_symbols)
        with model_subgraphs_ctl.solve(yield_=True) as hnd:
            model_found = False
            for model in hnd:
                model_found = True
                symbols = model.symbols(shown=True)
                reference_model_pg = symbols_to_prg(symbols)
                save_out(f"reference_model_{model.number}.lp", reference_model_pg)
                viz_graph(
                    pg=reference_model_pg,
                    graphs=["reference", "model(reference)"],
                    title="Reference Model Graph",
                    name=f"reference_model_pg_{model.number}",
                )
                foil_ctl = set_foil_ctl(
                    pg=reference_model_pg,
                    number_of_foils=self._number_explanations,
                    query_prg=query_prg,
                    distance_prg=distance_prg,
                )
                with foil_ctl.solve(yield_=True) as foil_hnd:
                    foil_found = False
                    for foil_model in foil_hnd:
                        foil_found = True
                        foil_model_pg = symbols_to_prg(list(foil_model.symbols(shown=True)))
                        save_out(f"foil_model_pg_{model.number}_{foil_model.number}.lp", foil_model_pg)
                        viz_graph(
                            pg=foil_model_pg,
                            graphs=["foil", "model(foil)"],
                            title="Foil Graph",
                            name=f"foil_model_pg_{model.number}_{foil_model.number}",
                        )
                        print_foil(foil_model_pg)
                        contrastive_pg = construct_contrastive(
                            pg=foil_model_pg,
                            query_prg=query_prg,
                        )
                        save_out(f"contrastive_{model.number}_{foil_model.number}.lp", contrastive_pg)
                        viz_graph(
                            pg=contrastive_pg,
                            graphs=["foil", "model(foil)", "reference", "model(reference)"],
                            title="Contrastive Graph",
                            name=f"contrastive_pg_{model.number}_{foil_model.number}",
                        )
                    if not foil_found:
                        log.warning("No foil found.")

            if not model_found:
                log.warning("UNSATISFIABLE. Will proceed to explain.")
                foil_ctl = set_foil_ctl(
                    pg=reference_pg,
                    number_of_foils=self._number_explanations,
                    query_prg=query_prg,
                    distance_prg=distance_prg,
                )
                with foil_ctl.solve(yield_=True) as foil_hnd:
                    foil_found = False
                    for foil_model in foil_hnd:
                        foil_found = True
                        foil_model_pg = symbols_to_prg(list(foil_model.symbols(shown=True)))
                        save_out(f"foil_model_pg_UNSAT_{foil_model.number}.lp", foil_model_pg)
                        viz_graph(
                            pg=foil_model_pg,
                            graphs=["foil", "model(foil)"],
                            title="Foil Graph",
                            name=f"foil_model_pg_UNSAT_{foil_model.number}",
                        )
                        print_foil(foil_model_pg)
                        contrastive_pg = construct_contrastive(
                            pg=foil_model_pg,
                            query_prg=query_prg,
                        )
                        save_out(f"contrastive_{foil_model.number}.lp", contrastive_pg)
                        viz_graph(
                            pg=contrastive_pg,
                            graphs=["foil", "model(foil)", "reference", "model(reference)"],
                            title="Contrastive Graph",
                            name=f"contrastive_pg_UNSAT_{foil_model.number}",
                        )
                    if not foil_found:
                        log.warning("No foil found.")
