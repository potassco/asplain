"""
Transformers used for generating the 'model support' reification.
"""

from clingo import ast

from asplain.utils.logging import get_logger
from .custom_transformer import CustomTransformer

WRAPPER_HYPOTHETICAL_PREDICATE_NAME = "hypothetical"
WRAPPER_MODEL_PREDICATE_NAME = "_model"
WRAPPER_ABDUCEDS_PREDICATE_NAME = "_abduced"

# Method name "visit_Rule" doesn't conform to snake_case naming style (invalid-name)
# Method name "visit_Literal" doesn't conform to snake_case naming style (invalid-name)
# pylint: disable=C0103

log = get_logger("main")


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

        # if rule.head.atom.ast_type == ast.ASTType.BooleanConstant:  # Integrity Constraint
        #     log.warning("Integrity constraints are ignored skiped rule: %s", rule)
        #     return ast.Comment(
        #         location=rule.location, value="% " + str(rule), comment_type=0  # ast.CommentType.Line = 0
        #     )

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

    @staticmethod
    def wrap_literal(literal: ast.AST) -> ast.AST:
        """
        Wraps the given `literal` in a hypothetical/1 predicate.
        """
        if (
            literal.ast_type == ast.ASTType.ConditionalLiteral
            and literal.literal.atom.symbol.name != WRAPPER_HYPOTHETICAL_PREDICATE_NAME
        ):
            return ast.ConditionalLiteral(
                location=literal.location,
                literal=HypotheticalLiteralsTransformer.wrap_literal(literal.literal),
                condition=[HypotheticalLiteralsTransformer.wrap_literal(lit) for lit in literal.condition],
            )

        if literal.ast_type == ast.ASTType.Literal and literal.atom.ast_type == ast.ASTType.BodyAggregate:
            elements = [
                ast.BodyAggregateElement(
                    terms=e.terms, condition=[HypotheticalLiteralsTransformer.wrap_literal(lit) for lit in e.condition]
                )
                for e in literal.atom.elements
            ]
            return ast.BodyAggregate(
                location=literal.location,
                left_guard=literal.atom.left_guard,
                function=literal.atom.function,
                elements=elements,
                right_guard=literal.atom.right_guard,
            )

        if (
            literal.ast_type == ast.ASTType.Literal
            and literal.atom.ast_type == ast.ASTType.SymbolicAtom
            and literal.atom.symbol.name != WRAPPER_HYPOTHETICAL_PREDICATE_NAME
        ):
            return ast.Literal(
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

    def visit_Literal(self, literal: ast.AST) -> ast.AST:
        """
        Wraps a literal within a hypothetical/1 predicate.
        """

        # if literal.atom.ast_type != ast.ASTType.SymbolicAtom:
        #     return literal

        # # Adds a wrapper predicate to the head of the rule
        # literal = ast.Literal(
        #     location=literal.location,
        #     sign=literal.sign,  # Positive literal
        #     atom=ast.Function(
        #         location=literal.location,
        #         name=WRAPPER_MODEL_PREDICATE_NAME,
        #         arguments=[
        #             ast.Function(
        #                 location=literal.location,
        #                 name=WRAPPER_HYPOTHETICAL_PREDICATE_NAME,
        #                 arguments=[],
        #                 external=False,
        #             ),
        #             literal.atom,
        #         ],
        #         external=False,
        #     ),
        # )
        return HypotheticalLiteralsTransformer.wrap_literal(literal)
