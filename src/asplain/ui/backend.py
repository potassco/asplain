from functools import cached_property

from clingo import Control, Function, String
from clingo.ast import Literal
from clinguin.server.application.backends import ClingoBackend
from clinguin.server.data.attribute import AttributeDao
from clinguin.utils import StandardTextProcessing, image_to_b64
from clinguin.utils.annotations import extends, overwrites
from clinguin.utils.transformer import UsesSignatureTransformer
from clorm import ConstantStr, Raw

from asplain import (
    construct_contrastive,
    construct_program_graph,
    set_foil_ctl,
    set_model_subgraphs_ctl,
)
from asplain.llm.models import ModelTag, OpenAIModel
from asplain.llm.templates import ExplainTemplate
from asplain.llm.utils import parse_llm_json_response
from asplain.utils.clingo import get_query_prg, symbols_to_prg
from asplain.utils.viz import viz_graph


class ASPlainBackend(ClingoBackend):
    """ASPlain backend for Clinguin server."""

    def _init_interactive(self):
        super()._init_interactive()
        self._query_include = []
        self._query_exclude = []
        self._explanation_handler = None
        self._explanation_iterator = None

        self._reference_model_pg = None
        self._reference_pg = None
        self._contrastive_pg = None
        self._foil_ctl = None

        self._llm_explanation = None
        self._active_llm = False

        self._engine = "dot"

        self._intermediate_format = "svg"
        self._attribute_image_key = "image_type"
        self._attribute_image_value = "clingraph"
        self._shown_graphs = [
            "reference",
            "model(reference)",
            "foil",
            "model(foil)",
            "contrastive",
        ]

    def _init_command_line(self):
        super()._init_command_line()
        self._dynamic_tags_files = self._args.dynamic_tags
        self._cost_encoding = self._args.cost_encoding

    @classmethod
    def register_options(cls, parser):
        ClingoBackend.register_options(parser)

        parser.add_argument(
            "--dynamic-tags",
            nargs="*",
            default=[],
            help="List of dynamic tags files to load.",
        )

        parser.add_argument(
            "--cost-encoding",
            nargs="*",
            default=[],
            help="List of cost encoding files to load.",
        )

    def _is_unsat(self) -> bool:
        return self._unsat_core is not None

    def _outdate_explanation(self):
        """
        Outdates all the dynamic values related to explanations when a change has been made.
        Any current interaction in the models wil be terminated by canceling the search and removing the iterator.
        """
        if self._explanation_handler:
            self._explanation_handler.cancel()
            self._explanation_handler = None
        self._explanation_iterator = None

        self._reference_model_pg = None
        self._reference_pg = None
        self._contrastive_pg = None

        self._outdate_llm_explanation()

    def _outdate_llm_explanation(self):
        self._llm_explanation = None
        self._clear_cache(["_ds_llm_explanation"])

    def _outdate(self):
        """
        Outdates all the dynamic values when a change has been made.
        Any current interaction in the models wil be terminated by canceling the search and removing the iterator.

        See Also:
                :func:`~_clear_cache`
        """
        super()._outdate()
        self._outdate_explanation()

    # def _get_shown_graphs(self):
    #     shown_graphs = list(self._shown_graphs)
    #     if self._explanation_iterator is None:
    #         if "foil" in shown_graphs:
    #             shown_graphs.remove("foil")
    #         if "model(foil)" in shown_graphs:
    #             shown_graphs.remove("model(foil)")
    #         if "contrastive" in shown_graphs:
    #             shown_graphs.remove("contrastive")
    #         if len(shown_graphs) == 0:
    #             shown_graphs.append("reference")
    #             shown_graphs.append("model(reference)")
    #     return shown_graphs

    @property
    def _ds_explanation(self):
        # Creates custom program
        # shown_graphs = self._get_shown_graphs()
        prg = get_query_prg(self._query_include, self._query_exclude)
        if self._explanation_iterator is None:
            self._update_reference_pg()
            self._contrastive_pg = self._reference_model_pg
            prg += "_no_foil."

        # prg += " ".join([f"show({g})." for g in shown_graphs])
        if self._contrastive_pg is not None:
            return prg + "\n" + self._contrastive_pg
        return prg

    @cached_property
    def _ds_llm_explanation(self):
        if self._active_llm:
            prg = "llm_active."

            if self._explanation_iterator is not None:
                self._logger.info("Generating LLM explanation...")
                program = str(self._ds_explanation)
                llm = OpenAIModel(model_tag=ModelTag.GPT_5)
                template = ExplainTemplate(contrastive_program_graph=program)

                response = llm.prompt_template_sync(template)
                explanation = parse_llm_json_response(response)
                self._llm_explanation = explanation
                prg += f'llm_explanation("{self._llm_explanation}"). llm_active.'
            return prg

        return ""

    def _init_ds_constructors(self):
        super()._init_ds_constructors()
        self._add_domain_state_constructor("_ds_explanation")
        self._add_domain_state_constructor("_ds_llm_explanation")

    # ---------------- Graph handling

    @extends(ClingoBackend)
    def _update_ui_state(self):
        """
        Updates the UI state by calling all domain state methods
        and creating a new control object (ui_control) using the ui_files provided
        """
        super()._update_ui_state()
        # domain_state = self._domain_state
        graphs = self._compute_clingraph_graphs()
        if graphs is None:
            return
        self._replace_uifb_with_b64_images_clingraph(graphs)

    def _compute_clingraph_graphs(self):
        """
        Computes all the graphs using the encoding and the domain state

        Arguments:

            domain_state (str): The model, brave, and cautious consequences (domain-state)
        """
        if not self._contrastive_pg:
            self._logger.info("No contrastive program graph to visualize")
            return None
        graphs = viz_graph(self._contrastive_pg, title="", name="pg")
        return graphs

    def _replace_uifb_with_b64_images_clingraph(self, graphs):
        """
        Replaces the clingraph predicates of the UI with the computed graphs.

        Arguments:
            graphs (dic) The computed graphs
        """
        attributes = list(self._ui_state.get_attributes(key=self._attribute_image_key))
        for attribute in attributes:
            attribute_value = StandardTextProcessing.parse_string_with_quotes(str(attribute.value))
            is_cg_image = attribute_value.startswith(self._attribute_image_value)

            if not is_cg_image:
                continue

            graph_name = "default"
            split = attribute_value.split("__")
            if len(split) > 1:
                graph_name = split[1]
            image_value = self._create_image_from_graph(graphs, key=graph_name)
            new_image_key = "image"
            base64_key_image = image_to_b64(image_value)

            new_attribute = AttributeDao(
                Raw(Function(str(attribute.id), [])),
                Raw(Function(str(new_image_key), [])),
                Raw(String(str(base64_key_image))),
            )
            self._ui_state.add_attribute_direct(new_attribute)

    def _create_image_from_graph(self, graphs, position=None, key=None):
        """
        Creates the image of the graph using clingraph

        Arguments:
            graphs (dic) The computed graphs
            position (int) The position of the graph to show
            key (int) The key of the graph to show
        """
        # graphs = graphs[0]
        if position is not None:
            if (len(graphs) - 1) >= position:
                graph = graphs[list(graphs.keys())[position]]
            else:
                self._logger.error("Attempted to access not valid position")
                raise Exception("Attempted to access not valid position")
        elif key is not None:
            if key in graphs:
                graph = graphs[key]
            else:
                self._logger.error("Key not found in graphs: %s", str(key))
                raise Exception("Key not found in graphs: " + str(key))
        else:
            self._logger.error("Must either specify position or key!")
            raise Exception("Must either specify position or key!")

        graph.format = self._intermediate_format
        img = graph.pipe(engine=self._engine)
        return img

    def _update_reference_pg(self):
        self._reference_pg = construct_program_graph(
            self._domain_files,
            constants=self._constants.items(),
            assumptions=self._assumptions,
            dynamic_tags_files=self._dynamic_tags_files,
        )

        self._reference_model_pg = None

        if not self._is_unsat():
            # print("----------Computing reference model graph")
            # print(self._model)
            model_subgraphs_ctl = set_model_subgraphs_ctl(pg=self._reference_pg, model_symbols=self._model)
            with model_subgraphs_ctl.solve(yield_=True) as hnd:
                for model in hnd:
                    # extract the model to print
                    self._reference_model_pg = symbols_to_prg(model.symbols(shown=True))
                    break

            if not self._reference_model_pg:
                self._logger.error(
                    "Expected model corresponding to reference with model membership for satisfiable instance"
                )
                self._reference_model_pg = self._reference_pg

    def _start_explanation(self):
        self._update_reference_pg()
        pg = self._reference_pg or ""
        if self._reference_model_pg is not None:
            pg += self._reference_model_pg
        cost_prg = ""
        if self._cost_encoding:
            for cost_file in self._cost_encoding:
                with open(cost_file, "r", encoding="utf-8") as cf:
                    cost_prg += cf.read() + "\n"
        self._foil_ctl = set_foil_ctl(
            pg=pg,
            query_prg=get_query_prg(self._query_include, self._query_exclude),
            number_of_foils=0,
            cost_prg=cost_prg,
        )
        self._explanation_handler = self._foil_ctl.solve(yield_=True)
        self._explanation_iterator = iter(self._explanation_handler)

    # --------------- Public

    def activate_llm(self, value=True) -> str:
        self._active_llm = False if value == False or value == "false" else True
        self._outdate_llm_explanation()

    # def add_shown_graph(self, value: str):
    #     """Add a graph to be shown in the UI."""
    #     if value not in self._shown_graphs:
    #         self._shown_graphs.append(value)

    # def remove_shown_graph(self, value: str):
    #     """Remove a graph from being shown in the UI."""
    #     if value in self._shown_graphs:
    #         self._shown_graphs.remove(value)

    def add_query(self, query: str, type: str):
        """Add a query to be included in the explanation."""
        assert type in ["true", "false"], "Type must be either include or exclude"
        if type == "true":
            if query not in self._query_include:
                self._query_include.append(query)
        else:
            if query not in self._query_exclude:
                self._query_exclude.append(query)
        self._explanation_handler = None
        self._explanation_iterator = None
        self._outdate_explanation()
        self.next_explanation()

    def remove_query(self, query: str):
        """Remove a query from the explanation."""
        if query in self._query_include:
            self._query_include.remove(query)
        if query in self._query_exclude:
            self._query_exclude.remove(query)
        self._outdate_explanation()
        self.next_explanation()

    def clear_queries(self):
        """Clear all queries."""
        self._query_include = []
        self._query_exclude = []
        self._outdate_explanation()

    def next_explanation(self):
        """Generate explanations interactively."""
        self._outdate_llm_explanation()
        # Implementation of explanation generation
        if self._explanation_iterator is None:
            self._start_explanation()
        try:
            foil_model = next(self._explanation_iterator)
            while not foil_model.optimality_proven:
                self._logger.info(
                    "Skipping intermediate none optimal model with cost %s...",
                    foil_model.cost,
                )
                foil_model = next(self._explanation_iterator)
            # print(foil_model.cost)
            foil_pg_and_model = foil_model.symbols(shown=True)  # shown should include the foil model and pg
            self._contrastive_pg = construct_contrastive(
                pg=symbols_to_prg(foil_pg_and_model),
                query_prg=get_query_prg(self._query_include, self._query_exclude),
            )
            self._logger.debug(self._contrastive_pg)

        except StopIteration:
            m = "No explanations"
            self._logger.error(m)
            self._outdate_explanation()
            self._messages.append(("Explanation Information", m, "info"))

    def download_explanation_graph(self, file_name: str):
        """Download the explanation graph as an image."""
        name = file_name.strip('"')
        viz_graph(
            self._contrastive_pg,
            title="",
            name=name,
            open=False,
            format="png",
        )
        self._messages.append(
            (
                "Download successful",
                f"Information saved in file out/{name}.png",
                "success",
            )
        )

    def download_explanation_facts(self, file_name: str):
        """Download the explanation facts."""
        pg = ""
        for g in self._get_shown_graphs():
            # TODO This should show all
            pg += "\n#show node(X,T):node(X,T).\n"
            pg += "\n#show edge(X,T):edge(X,T).\n"
            pg += "\n#show .\n"
        name = file_name.strip('"')
        ctl = Control()
        ctl.add("base", [], self._contrastive_pg + pg)
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            model = handle.model()
            model_symbols = model.symbols(shown=True)
            facts = symbols_to_prg(model_symbols)
            with open(f"out/{name}.lp", "w") as f:
                f.write(facts)
        self._messages.append(
            (
                "Download successful",
                f"Information saved in file out/{name}.lp",
                "success",
            )
        )
