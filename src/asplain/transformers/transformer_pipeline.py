"""
Provides a set of Pipelines of transformers for generating different reifications.
"""

from pathlib import Path
from typing import Sequence, Union

from clingo import ast
from clingo.ast import parse_files, parse_string

from .abduction_transformers import (
    AnnonymousVariablesRenamerTransformer,
    AbducedRemovedTransformer,
    HypotheticalLiteralsTransformer,
)
from .model_support_transformers import (
    CommentGenerator,
    ExplainabilityReifier,
    ModelLiteralTransformer,
    WorldVariableSafetyTransformer,
)


class TransformerPipeline:
    """
    A class that applies a sequence of transformers to a program.
    """

    def __init__(self, transformers: Sequence[ast.Transformer]) -> None:
        self.transformers = transformers

    def _apply_transformers(self, stm: ast.AST) -> list[ast.AST]:
        """
        Applies the transformers to the given program.
        May generate multiple elements when at least of the transformers generates multiple elements.
        """
        pipes = [stm]
        for transformer in self.transformers:
            new_pipes = []
            for element in pipes:
                # Transform the element
                transformed = transformer(element)
                # Set new pipes if multiple transformed elements
                new_pipes.extend([transformed] if not hasattr(transformed, "__iter__") else list(transformed))
            pipes = new_pipes
        return pipes

    def parse_string(self, string: str) -> str:
        """
        Applies the transformers to the program string.
        """
        out = []
        parse_string(
            string,
            lambda stm: out.extend([str(new_stm) for new_stm in self._apply_transformers(stm)]),
        )
        return "\n".join(out)

    def parse_files(self, paths: Sequence[Union[str, Path]]) -> str:
        """
        Applies the transformers to the program files.
        """
        out = []
        parse_files(
            [str(p) for p in paths],
            lambda stm: out.extend([str(new_stm) for new_stm in self._apply_transformers(stm)]),
        )
        return "\n".join(out)


class AbductionPipeline(TransformerPipeline):
    """
    Reifies the abduction program.
    """

    def __init__(self) -> None:
        super().__init__(
            [
                AnnonymousVariablesRenamerTransformer(),
                AbducedRemovedTransformer(),
                HypotheticalLiteralsTransformer(),
            ]
        )


class ModelSupportPipeline(TransformerPipeline):
    """
    Reifies the model support program. This program includes the positive and negative dependencies among the atoms.
    """

    def __init__(self) -> None:
        super().__init__(
            [
                AnnonymousVariablesRenamerTransformer(),
                CommentGenerator(),
                ExplainabilityReifier(),
                ModelLiteralTransformer(),
                WorldVariableSafetyTransformer(),
            ]
        )
