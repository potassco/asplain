"""
Classes that do the explanation of the models.
"""

from typing import Sequence

from ..utils.logging import get_logger

log = get_logger("main")


class Explainer:
    """
    Basic class for any explainer.
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

    def explain(
        self, model_symbols: Sequence[str], query_include: Sequence[str], query_exclude: Sequence[str]
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
        raise NotImplementedError

    def viz_explanation_graph(self, explanation_graph: str, name: str = "explanation") -> None:
        """
        Visualize the explanation graph using cligraph

        Args:
            explanation_graph: The explanation graph to visualize.
            name: The name of the output file. File will be stored in the same directory
                    as the domain files, inside the `out` directory.
        """

        raise NotImplementedError
