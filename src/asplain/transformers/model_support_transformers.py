"""
Transformers used for generating the 'model support' reification.
"""

from typing import Generator, Sequence, Union

from clingo import Number, ast

from asplain.utils.logging import get_logger

from ._ast_shortcuts import aggregates_elements, collect_free_vars, conditional_literals, inhibits, propagates
from .custom_transformer import CustomTransformer, GeneratorTransformer

MODEL_WRAPPER_PREDICATE_NAME = "_model"
WORLD_PREDICATE_NAME = "world"
WORLD_VARIABLE_NAME = "World"

SUPPORT_RULE_PREDICATE_NAME = "_sup"
SUPPORT_CONSTRAINT_PREDICATE_NAME = "_sup_constraint"
DEPENDS_RULE_PREDICATE_NAME = "_depends"
PREVENTS_RULE_PREDICATE_NAME = "_prevents"
CONSTRAINTS_RULE_PREDICATE_NAME = "_constraints"

log = get_logger("main")

# Method name "visit_Rule" doesn't conform to snake_case naming style (invalid-name)
# pylint: disable=C0103


class ImplicitChoiceConstraintsTransformer(GeneratorTransformer):
    def visit_Rule(self, rule: ast.AST) -> Generator[ast.AST, None, None]:
        """
        Generates the cardinality constraints for choice rules that are implicit.
        Example:
        ```
        % Program
        Lower { a; b } Upper :- conditions.

        % Replacement
        { a; b } :- conditions.
        :- #count{a;b}>Upper, conditions.
        :- #count{a;b}<Lower, conditions.
        ```
        """
        # Any rule is returned as it is
        yield rule

        # If it is a choice rule, we generate the corresponding cardinality constraints
        if rule.head.ast_type == ast.ASTType.Aggregate:
            false_head = ast.Literal(
                location=rule.head.location,
                sign=False,  # Positive literal
                atom=ast.BooleanConstant(0),
            )

            # Convert cond literals in body aggregate elements for correct body asts
            agg_elements = [
                ast.BodyAggregateElement(
                    terms=[cond_lit.literal.atom],
                    condition=[cond_lit.literal] + list(cond_lit.condition),
                )
                for cond_lit in rule.head.elements
            ]

            if rule.head.left_guard is not None:
                # Yield Constraint for Lower Bound
                lower_bound = int(str(rule.head.left_guard.term))
                lowerbound_count_literal = ast.Literal(
                    location=rule.body[0].location,
                    sign=False,  # Positive literal
                    atom=ast.BodyAggregate(
                        location=rule.body[0].location,
                        elements=agg_elements,
                        function=0,  # count type
                        left_guard=ast.Guard(
                            comparison=ast.ComparisonOperator.LessThan,
                            term=ast.SymbolicTerm(
                                location=rule.body[0].location,
                                symbol=Number(lower_bound),
                            ),
                        ),
                        right_guard=None,
                    ),
                )
                lower_bound_constraint = ast.Rule(
                    location=rule.location,
                    head=false_head,
                    body=[lowerbound_count_literal] + list(rule.body),
                )
                yield lower_bound_constraint

            if rule.head.right_guard is not None:
                # Yield Constraint for Upper Bound
                upper_bound = int(str(rule.head.right_guard.term))
                upperbound_count_literal = ast.Literal(
                    location=rule.body[0].location,
                    sign=False,  # Positive literal
                    atom=ast.BodyAggregate(
                        location=rule.body[0].location,
                        elements=agg_elements,
                        function=0,  # count type
                        left_guard=ast.Guard(
                            comparison=ast.ComparisonOperator.GreaterThan,
                            term=ast.SymbolicTerm(
                                location=rule.body[0].location,
                                symbol=Number(upper_bound),
                            ),
                        ),
                        right_guard=None,
                    ),
                )
                upper_bound_constraint = ast.Rule(
                    location=rule.location,
                    head=false_head,
                    body=[upperbound_count_literal] + list(rule.body),
                )
                yield upper_bound_constraint


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
        if rule.head.atom.name in [
            DEPENDS_RULE_PREDICATE_NAME,
            PREVENTS_RULE_PREDICATE_NAME,
            CONSTRAINTS_RULE_PREDICATE_NAME,
        ]:
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
    def wrap_literal(literal: ast.AST, hybrid_worlds: bool = False) -> ast.AST:
        """
        Wraps the given `literal` in a _model/2 predicate.
        """
        if (
            literal.ast_type == ast.ASTType.ConditionalLiteral
            and literal.literal.atom.symbol.name != MODEL_WRAPPER_PREDICATE_NAME
        ):
            return ast.ConditionalLiteral(
                location=literal.location,
                literal=ModelLiteralTransformer.wrap_literal(literal.literal, hybrid_worlds=hybrid_worlds),
                condition=[
                    ModelLiteralTransformer.wrap_literal(lit, hybrid_worlds=hybrid_worlds) for lit in literal.condition
                ],
            )

        if literal.ast_type == ast.ASTType.Literal and literal.atom.ast_type == ast.ASTType.BodyAggregate:
            elements = [
                ast.BodyAggregateElement(
                    terms=e.terms,
                    condition=[
                        ModelLiteralTransformer.wrap_literal(lit, hybrid_worlds=hybrid_worlds) for lit in e.condition
                    ],
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
            and literal.atom.symbol.name != MODEL_WRAPPER_PREDICATE_NAME
        ):
            return ast.Literal(
                location=literal.location,
                sign=literal.sign,  # Positive literal
                atom=ast.Function(
                    location=literal.location,
                    name=MODEL_WRAPPER_PREDICATE_NAME,
                    arguments=[
                        ast.Variable(location=literal.location, name="_" if hybrid_worlds else WORLD_VARIABLE_NAME),
                        literal.atom,
                    ],
                    external=False,
                ),
            )

        return literal

    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        """
        Returns the rule but wraps every literal in the body in a _model/2 predicate.
        """
        if rule.head.ast_type != ast.ASTType.Literal:
            return rule

        # # To ignore rules
        # if rule.head.atom.name in [
        #     DEPENDS_RULE_PREDICATE_NAME,
        #     PREVENTS_RULE_PREDICATE_NAME,
        # ]:
        #     return rule

        hybrid_worlds = False
        if rule.head.atom.name in (CONSTRAINTS_RULE_PREDICATE_NAME, SUPPORT_CONSTRAINT_PREDICATE_NAME):
            hybrid_worlds = True

        new_body = []
        for literal in rule.body:
            new_body.append(ModelLiteralTransformer.wrap_literal(literal, hybrid_worlds=hybrid_worlds))

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
        self.constraint_count = 0

    def _generate_support_rule(
        self,
        supported_lit: ast.AST,
        rule_body: Sequence[ast.AST],
    ) -> ast.AST:
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
        support_literal: ast.AST,
        predicate_name: str,
        dependencies: Sequence[ast.AST],
        extra_body: Sequence[ast.AST],
    ) -> Union[ast.AST, None]:
        """
        Creates a particular dependency rule, from a given support rule.
        """
        if len(dependencies) == 0:
            return None

        dependency_literal = ast.Literal(
            location=support_literal.location,
            sign=False,  # Positive Literal
            atom=ast.Function(
                location=(support_literal.location),
                name=predicate_name,
                arguments=[
                    support_literal,
                    ast.Pool(support_literal.location, dependencies),
                ],
                external=False,
            ),
        )

        # Creates the new rule
        return ast.Rule(
            location=support_literal.location,
            head=dependency_literal,
            # body=[ModelLiteralTransformer.wrap_literal(lit) for lit in extra_body] + [support_literal],
            body=extra_body + [support_literal],
        )

    def _generate_fired_contrastive_constraint(self, lit_sequecence: Sequence[ast.AST]) -> ast.AST:
        """
        Creates a rule featuring the predicate _fired_contrastive_constraint/2.
          _fired_constrastive_constraint((ConstraintID, VariableValues), Atom)
        identifies the possible firing of a constraint of the original program
        when both worlds 'real' and 'hypothetical' are considered simultaneously.
            - The tuple (ConstraintID, VariableValues) identifies a particular
              firing of such a constraint.
            - Atom: captures the related atoms that collaborated in the firing of
              the constraint.
        """
        # Increments the constraint count
        self.constraint_count += 1

        loc = lit_sequecence[0].location
        # head = ast.Literal(
        #     location=loc,
        #     sign=False,  # Positive Literal
        #     atom=ast.Function(
        #         location=loc,
        #         name=SUPPORT_CONSTRAINT_PREDICATE_NAME,
        #         arguments=[
        #             ast.Function(  # (ConstraintID, VariableValues)
        #                 location=loc,
        #                 name="",  # For creating a tuple
        #                 arguments=[
        #                     ast.SymbolicTerm(
        #                         location=loc,
        #                         symbol=Number(self.constraint_count),
        #                     ),
        #                     ast.Function(
        #                         location=loc,
        #                         name="",
        #                         arguments=list(collect_free_vars(lit_sequecence, [])),
        #                         external=False,
        #                     ),
        #                 ],
        #                 external=False,
        #             ),
        #             ast.Pool(loc, list(propagates(lit_sequecence))),  # Atom
        #         ],
        #         external=False,
        #     ),
        # )

        head = ast.Literal(
            location=loc,
            sign=False,  # Positive Literal
            atom=ast.Function(
                location=loc,
                name=SUPPORT_CONSTRAINT_PREDICATE_NAME,
                arguments=[
                    ast.SymbolicTerm(
                        location=loc,
                        symbol=Number(self.constraint_count),
                    ),
                    ast.Function(
                        location=loc,
                        name="",
                        arguments=list(collect_free_vars(lit_sequecence, [])),
                        external=False,
                    ),
                ],
                external=False,
            ),
        )

        # Creates the new rule
        return ast.Rule(
            location=loc,
            head=head,
            body=lit_sequecence,
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
            return

        elif rule.head.ast_type == ast.ASTType.Literal:  # Non-disjunctive head
            supported_atoms.append(rule.head)
            additional_causes.append([])
        else:
            raise NotImplementedError(f"Rules with a head of type {rule.head.ASTType} are not supported yet")

        # For each supported atom, we create a new rule.
        for lit, choice_condition in zip(supported_atoms, additional_causes):
            # Constraints
            if lit.atom.ast_type == ast.ASTType.BooleanConstant:
                support_rule = self._generate_fired_contrastive_constraint(rule.body)
                dependency_predicate = CONSTRAINTS_RULE_PREDICATE_NAME
            else:
                support_rule = self._generate_support_rule(lit, list(rule.body) + choice_condition)
                dependency_predicate = DEPENDS_RULE_PREDICATE_NAME

                # Yield Prevents Rule (if we have inhibitors)
                prevents_rule = self._generate_dependency_rule(
                    support_rule.head,
                    PREVENTS_RULE_PREDICATE_NAME,
                    list(inhibits(rule.body)),  # Dependencies
                    [],  # Body of the dependency rule
                )
                if prevents_rule is not None:
                    yield prevents_rule

            # Yield Support Rule
            yield support_rule

            # Yield Depends Rule for the body of the rule (if we have dependencies)
            depends_rule = self._generate_dependency_rule(
                support_rule.head,
                dependency_predicate,
                list(propagates(support_rule.body)),  # Causes
                [],  # Body of the dependency rule
            )
            if depends_rule is not None:
                yield depends_rule

            # Yield Depends rule for each conditional literal in the body
            for conditional_lit in conditional_literals(rule.body):
                depends_rule = self._generate_dependency_rule(
                    support_rule.head,
                    dependency_predicate,
                    [conditional_lit.literal] + list(propagates(conditional_lit.condition)),  # Dependencies
                    list(conditional_lit.condition),  # Body of the dependency rule
                )
                if depends_rule is not None:
                    yield depends_rule

            # Yield Depends rule for each BodyAggregateElement in the body
            for agg_element in aggregates_elements(rule.body):
                depends_rule = self._generate_dependency_rule(
                    support_rule.head,
                    dependency_predicate,
                    list(propagates(agg_element.condition)),  # Dependencies
                    list(agg_element.condition),  # Body of the dependency rule
                )
                if depends_rule is not None:
                    yield depends_rule
