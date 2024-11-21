from typing import Sequence, Union
from pathlib import Path

from clingo.ast import parse_string, parse_files
from clingo import ast

from .abduction_transformers import HypotheticalLiteralsTransformer, AbducedRemovedTransformer
from .model_support_transformers import (
    ModelLiteralTransformer,
    WorldVariableSafeTransformer,
    SupportRuleTransformer,
    DependenciesTransformer,
    CommentGenerator,
)


class TransformerPipeline:
    """
    A class that applies a sequence of transformers to a program.
    """

    def __init__(self, transformers):
        self.transformers = transformers

    def _apply_transformers(self, stm):
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

    def __init__(self):
        super().__init__(
            [
                AbducedRemovedTransformer(),
                HypotheticalLiteralsTransformer(),
            ]
        )


class ModelSupportPipeline(TransformerPipeline):
    """
    Reifies the model support program.
    """

    def __init__(self):
        super().__init__(
            [
                CommentGenerator(),
                SupportRuleTransformer(),
                DependenciesTransformer(),
                ModelLiteralTransformer(),
                WorldVariableSafeTransformer(),
            ]
        )
