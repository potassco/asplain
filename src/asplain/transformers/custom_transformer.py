from pathlib import Path
from typing import Sequence, Union

from clingo import ast


class CustomTransformer(ast.Transformer):
    """
    Provides an abstraction for our transformers. The class contains some common methods to parse strings and files.
    """

    def parse_string(self, string: str) -> str:
        out = []
        ast.parse_string(string, lambda stm: out.append(str(self(stm))))
        return "\n".join(out)

    def parse_files(self, paths: Sequence[Union[str, Path]]) -> str:
        out = []
        ast.parse_files(
            [str(p) for p in paths],
            lambda stm: out.append(str(self(stm))),
        )
        return "\n".join(out)


class GeneratorTransformer(ast.Transformer):
    """
    Provides an abstraction for an special type of transformers, which do not modify the incoming rules but generate new ones.
    When `parse_string` or `parse_files` are passed, we assume that `self(stm)` will return a generator of ASTs instead of
    returning one AST.
    """

    def parse_string(self, string: str) -> str:
        out = []
        ast.parse_string(string, lambda stm: out + list(str(ast_elem) for ast_elem in self(stm)))
        return "\n".join(out)

    def parse_files(self, paths: Sequence[Union[str, Path]]) -> str:
        out = []
        ast.parse_files(
            [str(p) for p in paths],
            lambda stm: out + list(str(ast_elem) for ast_elem in self(stm)),
        )
        return "\n".join(out)
