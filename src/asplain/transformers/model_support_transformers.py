"""
Transformers used for generating the 'model support' reification.
"""

from typing import Callable, Sequence, Union, Generator

from clingo import Number, ast

from asplain.utils.logging import get_logger

from ._ast_shortcuts import collect_free_vars, inhibits, propagates
from .custom_transformer import CustomTransformer, GeneratorTransformer

MODEL_WRAPPER_PREDICATE_NAME = "_model"
WORLD_PREDICATE_NAME = "world"
WORLD_VARIABLE_NAME = "World"

SUPPORT_RULE_PREDICATE_NAME = "_sup"
DEPENDS_RULE_PREDICATE_NAME = "_depends"
PREVENTS_RULE_PREDICATE_NAME = "_prevents"

log = get_logger("main")

# Method name "visit_Rule" doesn't conform to snake_case naming style (invalid-name)
# pylint: disable=C0103


class WorldVariableSafetyTransformer(CustomTransformer):
    """
    Creates a literal `world(World)` in the body of each rule for safety.
    """

    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        """
        Creates a new literal `world(World)` in the body of the given rule.
        """
        if rule.head.ast_type != ast.ASTType.Literal:
            return rule

        # To ignore rules
        if rule.head.atom.name in [DEPENDS_RULE_PREDICATE_NAME, PREVENTS_RULE_PREDICATE_NAME]:
            return rule

        # Creates new literal for the body (not _abduced(rm, Head))
        world_literal = ast.Literal(
            location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
            sign=False,  # Positive Literal
            atom=ast.Function(
                location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                name=WORLD_PREDICATE_NAME,
                arguments=[
                    ast.Variable(
                        location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                        name=WORLD_VARIABLE_NAME,
                    )
                ],
                external=False,
            ),
        )

        # Creates the new rule
        rule = ast.Rule(
            location=rule.location,
            head=rule.head,
            body=[world_literal] + list(rule.body),
        )

        return rule


class ModelLiteralTransformer(CustomTransformer):
    """
    Wraps each literal in the body of the rules in a program within a _model/2 predicate.
    """

    @staticmethod
    def _wrap_literal(literal: ast.AST) -> ast.AST:
        """
        Wraps the given `literal` in a _model/2 predicate.
        """
        return ast.Literal(
            location=literal.location,
            sign=literal.sign,  # Positive literal
            atom=ast.Function(
                location=literal.location,
                name=MODEL_WRAPPER_PREDICATE_NAME,
                arguments=[
                    ast.Variable(location=literal.location, name=WORLD_VARIABLE_NAME),
                    literal.atom,
                ],
                external=False,
            ),
        )

    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        """
        Returns the rule but wraps every literal in the body in a _model/2 predicate.
        """
        if rule.head.ast_type != ast.ASTType.Literal:
            return rule

        # To ignore rules
        if rule.head.atom.name in [DEPENDS_RULE_PREDICATE_NAME, PREVENTS_RULE_PREDICATE_NAME]:
            return rule

        new_body = []
        for literal in rule.body:
            if (
                literal.atom.ast_type == ast.ASTType.SymbolicAtom
                and literal.atom.symbol.name != MODEL_WRAPPER_PREDICATE_NAME
            ):
                new_body.append(self._wrap_literal(literal))
            else:
                new_body.append(literal)

        # Creates the new rule
        rule = ast.Rule(
            location=rule.location,
            head=rule.head,
            body=new_body,
        )

        return rule


class CommentGenerator(GeneratorTransformer):
    """
    Generates a comment comprising the original rule.
    """

    def visit_Rule(self, rule: ast.AST) -> Generator[ast.AST, None, None]:
        """
        Generates a comment for the given rule and then yields the original rule.
        """
        yield ast.Comment(location=rule.location, value="% " + str(rule), comment_type=0)  # ast.CommentType.Line = 0
        yield rule


class ExplainabilityReifier(GeneratorTransformer):
    """
    Generates the Explainability Reification.
    For each rule, generates:
        - **Support_rule**: `_sup(RuleID, World, SupportedAtom, VariableValues)` (from 1 to *N*, where *N* is the
          number of elements in the disjunction or the number of conditional literals inside the head's choice).
        - **Depends_rule**: `_depends(SupportLiteral, CausesPool)` (from 0 to 1, for each generated support rule).
        - **Prevents_rule**: `_prevents(SupportLiteral, InhibitorsPool)` (from 0 to 1, for each generated support rule).
    """

    def __init__(self) -> None:
        self.rule_count = 0

    def _generate_support_rule(self, supported_lit: ast.AST, rule_body: ast.ASTSequence) -> ast.AST:
        """
        Creates the support rule from an original rule.
        """
        # Increments rule count
        self.rule_count += 1

        # Creates new head _sup(RuleID, World, SupportedAtom, VariableValues)
        xclingo_sup_literal = ast.Literal(
            location=rule_body[0].location if len(rule_body) > 0 else supported_lit.location,
            sign=False,  # Positive Literal
            atom=ast.Function(
                location=rule_body[0].location if len(rule_body) > 0 else supported_lit.location,
                name=SUPPORT_RULE_PREDICATE_NAME,
                arguments=[
                    ast.SymbolicTerm(
                        location=rule_body[0].location if len(rule_body) > 0 else supported_lit.location,
                        symbol=Number(self.rule_count),
                    ),
                    ast.Variable(
                        location=rule_body[0].location if len(rule_body) > 0 else supported_lit.location,
                        name=WORLD_VARIABLE_NAME,
                    ),
                    supported_lit,
                    ast.Function(
                        location=rule_body[0].location if len(rule_body) > 0 else supported_lit.location,
                        name="",  # For creating a tuple
                        arguments=list(collect_free_vars(rule_body, [])),
                        external=False,
                    ),
                ],
                external=False,
            ),
        )

        # Creates the new support rule
        support_rule = ast.Rule(
            location=supported_lit.location,
            head=xclingo_sup_literal,
            body=rule_body,
        )

        return support_rule

    def _generate_dependency_rule(
        self,
        support_rule: ast.AST,
        predicate_name: str,
        dependency_catcher: Callable[[Sequence[ast.AST]], Generator[ast.AST, None, None]],
        additional_causes: list[ast.AST],
    ) -> Union[ast.AST, None]:
        """
        Creates a particular dependency rule, from a given support rule.
        """
        dependencies = list(dependency_catcher(support_rule.body)) + additional_causes
        if len(dependencies) == 0:
            return None

        dependency_literal = ast.Literal(
            location=support_rule.body[0].location if len(support_rule.body) > 0 else support_rule.head.location,
            sign=False,  # Positive Literal
            atom=ast.Function(
                location=(support_rule.body[0].location if len(support_rule.body) > 0 else support_rule.head.location),
                name=predicate_name,
                arguments=[
                    support_rule.head,
                    ast.Pool(support_rule.head.location, dependencies),
                ],
                external=False,
            ),
        )

        # Creates the new rule
        return ast.Rule(
            location=support_rule.location,
            head=dependency_literal,
            body=[support_rule.head],
        )

    def visit_Rule(self, rule: ast.AST) -> Generator[ast.AST, None, None]:
        """
        Generates the support rule, and every needed depends and prevents rules.
        """
        supported_atoms = []
        additional_causes = []

        if rule.head.ast_type == ast.ASTType.Aggregate:  # Choices
            for conditional_lit in rule.head.elements:
                supported_atoms.append(conditional_lit.literal)
                additional_causes.append(list(propagates(conditional_lit.condition)))

        elif rule.head.ast_type == ast.ASTType.Disjunction:  # Disjunctive head
            log.warning("Disjunction not supported yet, skiped rule: %s", rule)
            yield rule

        elif rule.head.ast_type == ast.ASTType.Literal:  # Non-disjunctive head
            supported_atoms.append(rule.head)
            additional_causes.append([])
        else:
            raise NotImplementedError(f"Rules with a head of type {rule.head.ASTType} are not supported yet")

        # For each supported atom, we create a new rule.
        for lit, choice_causes in zip(supported_atoms, additional_causes):
            support_rule = self._generate_support_rule(lit, rule.body)
            # Yield Support Rule
            yield support_rule
            # Yield Depends Rule (if we have dependencies)
            depends_rule = self._generate_dependency_rule(
                support_rule, DEPENDS_RULE_PREDICATE_NAME, propagates, choice_causes
            )
            if depends_rule is not None:
                yield depends_rule
            # Yield Prevents Rule (if we have inhibitors)
            prevents_rule = self._generate_dependency_rule(support_rule, PREVENTS_RULE_PREDICATE_NAME, inhibits, [])
            if prevents_rule is not None:
                yield prevents_rule
