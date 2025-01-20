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
        head = rule.head
        extra_body = []

        if rule.head.ast_type == ast.ASTType.Aggregate:  # Choices
            new_elements = []
            for conditional_lit in rule.head.elements:
                not_removed_literal = ast.Literal(
                    location=conditional_lit.literal.location,
                    sign=True,  # Negative Literal
                    atom=ast.Function(
                        location=conditional_lit.literal.location,
                        name=WRAPPER_ABDUCEDS_PREDICATE_NAME,
                        arguments=[
                            ast.Function(
                                location=conditional_lit.literal.location,
                                name="rm",
                                arguments=[],
                                external=False,
                            ),
                            conditional_lit.literal.atom,
                        ],
                        external=False,
                    ),
                )
                new_elements.append(
                    ast.ConditionalLiteral(
                        location=conditional_lit.location,
                        literal=conditional_lit.literal,
                        condition=[not_removed_literal] + list(conditional_lit.condition),
                    )
                )
            # Updates the head
            head = ast.Aggregate(
                location=head.location,
                left_guard=head.left_guard,
                elements=new_elements,
                right_guard=head.right_guard,
            )

        if rule.head.ast_type == ast.ASTType.Literal:
            if rule.head.atom.ast_type == ast.ASTType.BooleanConstant:  # Integrity Constraint
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

            extra_body.append(not_removed_literal)

        # Creates the new rule
        rule = ast.Rule(
            location=rule.location,
            head=head,  # Uses either the original head or the updated head
            body=extra_body + list(rule.body),
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
        if literal.ast_type == ast.ASTType.ConditionalLiteral:
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

        if literal.ast_type == ast.ASTType.Literal:  # Also Pools
            # Skip 'not _abduced(rm, Head)'
            if (
                literal.atom.ast_type == ast.ASTType.Function
                and literal.sign == 1  # Negative literal
                and literal.atom.name == WRAPPER_ABDUCEDS_PREDICATE_NAME
            ):
                return literal

            if literal.atom.ast_type == ast.ASTType.BooleanConstant:  # Integrity Constraint Head
                return literal

            if literal.atom.ast_type == ast.ASTType.Comparison:
                return literal

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

        return HypotheticalLiteralsTransformer.wrap_literal(literal)


class AnnonymousVariablesRenamerTransformer(CustomTransformer):

    def __init__(self) -> None:
        self.annon_count = 0

    def visit_Variable(self, variable: ast.AST) -> ast.AST:
        """
        Renames the anonymous variables to avoid conflicts.
        """

        if variable.name == "_":
            self.annon_count += 1
            new_name = f"_Annon_{self.annon_count}"
            return ast.Variable(location=variable.location, name=new_name)

        return variable
