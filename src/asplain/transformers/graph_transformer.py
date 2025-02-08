"""
Transformers used for generating the 'model support' reification.
"""

from clingo import Number, String, ast

from .custom_transformer import CustomTransformer, GeneratorTransformer


class GraphTransformer(CustomTransformer):
    """
    Transformer to tag head and body occurrences of `&diff` atoms.
    """

    def __init__(self):
        super().__init__()
        self.edge_ids = {}

    def _get_new_id(self, edge_id: str, loc: ast.Location) -> ast.SymbolicTerm:
        """
        Get the new id for the edge.
        """
        if edge_id not in self.edge_ids:
            self.edge_ids[edge_id] = len(self.edge_ids)
        return ast.SymbolicTerm(location=loc, symbol=Number(self.edge_ids[edge_id]))

    def visit_Literal(self, lit: ast.AST, in_lit: bool = False) -> ast.AST:
        """
        Visit literal; any theory atom in a literal is a body literal.
        """
        symbol = lit.atom.symbol
        if symbol.name == "edge":
            edge_id = symbol.arguments[2]
            new_id = self._get_new_id(edge_id, lit.location)
            return ast.Literal(
                location=lit.location,
                sign=lit.sign,  # Positive lit
                atom=ast.Function(
                    location=lit.location,
                    name=symbol.name,
                    arguments=[
                        symbol.arguments[0],
                        symbol.arguments[1],
                        new_id,
                    ],
                    external=False,
                ),
            )
        if symbol.name == "attr" and symbol.arguments[0].symbol.name == "edge":
            edge_id = symbol.arguments[1]
            new_id = self._get_new_id(edge_id, lit.location)
            return ast.Literal(
                location=lit.location,
                sign=lit.sign,  # Positive lit
                atom=ast.Function(
                    location=lit.location,
                    name=symbol.name,
                    arguments=[
                        symbol.arguments[0],
                        new_id,
                        symbol.arguments[2],
                        symbol.arguments[3],
                    ],
                    external=False,
                ),
            )
            return lit
        return lit
