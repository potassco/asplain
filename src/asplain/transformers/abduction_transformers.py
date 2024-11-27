"""
Transformers used for generating the 'model support' reification.
"""

from clingo import ast

from .custom_transformer import CustomTransformer

WRAPPER_HYPOTHETICAL_PREDICATE_NAME = "hypothetical"
WRAPPER_MODEL_PREDICATE_NAME = "_model"
WRAPPER_ABDUCEDS_PREDICATE_NAME = "_abduced"

# Method name "visit_Rule" doesn't conform to snake_case naming style (invalid-name)
# Method name "visit_Literal" doesn't conform to snake_case naming style (invalid-name)
# pylint: disable=C0103


class AbducedRemovedTransformer(CustomTransformer):
    """
    Adds a special literal `not _abduced(rm, Head)` in the body of each rule, allowing the removing of some atoms when
    abducing.
    """

    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        """
        Creates a special literal `not _abduced(rm, Head)` in the body of each rule, allowing the removing of some
        atoms when abducing.
        """
        if rule.head.ast_type != ast.ASTType.Literal:
            return rule
        # Creates new literal for the body (not _abduced(rm, Head))
        not_removed_literal = ast.Literal(
            location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
            sign=True,  # Negative Literal
            atom=ast.Function(
                location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                name=WRAPPER_ABDUCEDS_PREDICATE_NAME,
                arguments=[
                    ast.Function(
                        location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                        name="rm",
                        arguments=[],
                        external=False,
                    ),
                    rule.head.atom,
                ],
                external=False,
            ),
        )

        # Creates the new rule
        rule = ast.Rule(
            location=rule.location,
            head=rule.head,
            body=[not_removed_literal] + list(rule.body),
        )

        return rule


class HypotheticalLiteralsTransformer(CustomTransformer):
    """
    Wraps each literal in a program within a hypothetical/1 predicate.
    """

    def visit_Literal(self, literal: ast.AST) -> ast.AST:
        """
        Wraps a literal within a hypothetical/1 predicate.
        """
        if literal.atom.ast_type != ast.ASTType.SymbolicAtom:
            return literal
        # Adds a wrapper predicate to the head of the rule
        literal = ast.Literal(
            location=literal.location,
            sign=literal.sign,  # Positive literal
            atom=ast.Function(
                location=literal.location,
                name=WRAPPER_MODEL_PREDICATE_NAME,
                arguments=[
                    ast.Function(
                        location=literal.location,
                        name=WRAPPER_HYPOTHETICAL_PREDICATE_NAME,
                        arguments=[],
                        external=False,
                    ),
                    literal.atom,
                ],
                external=False,
            ),
        )
        return literal
