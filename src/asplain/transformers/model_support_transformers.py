from typing import Union

from clingo import Number, ast

from ._ast_shortcuts import collect_free_vars, inhibits, propagates
from .custom_transformer import CustomTransformer, GeneratorTransformer

MODEL_WRAPPER_PREDICATE_NAME = "_model"
WORLD_PREDICATE_NAME = "world"
WORLD_VARIABLE_NAME = "World"

SUPPORT_RULE_PREDICATE_NAME = "_sup"
DEPENDS_RULE_PREDICATE_NAME = "_depends"
PREVENTS_RULE_PREDICATE_NAME = "_prevents"


class WorldVariableSafeTransformer(CustomTransformer):
    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        """
        Creates a literal `world(World)` in the body of each rule for safety.
        """
        if rule.head.ast_type != ast.ASTType.Literal:  # TODO: Which expressions fall here?
            return rule
        else:
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
    @staticmethod
    def _wrap_literal(literal: ast.AST) -> ast.AST:
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

    def visit_Rule(self, rule: ast.AST) -> ast.Sequence:
        if rule.head.ast_type != ast.ASTType.Literal:  # TODO: Which expressions fall here?
            return rule
        else:
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
    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        yield ast.Comment(location=rule.location, value="% " + str(rule), comment_type=0)  # ast.CommentType.Line = 0
        yield rule


class SupportRuleTransformer(CustomTransformer):
    def __init__(self):
        self.rule_count = 0

    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        """
        Creates a special literal `not _abduced(rm, Head)` in the body of each rule, allowing the removing of some atoms when abducing.
        """
        if rule.head.ast_type != ast.ASTType.Literal:  # TODO: Which expressions fall here?
            return rule
        else:
            # Increments rule count
            self.rule_count += 1

            # Creates new head _sup(RuleID, World, SupportedAtom, VariableValues)
            xclingo_sup_literal = ast.Literal(
                location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                sign=False,  # Positive Literal
                atom=ast.Function(
                    location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                    name=SUPPORT_RULE_PREDICATE_NAME,
                    arguments=[
                        ast.SymbolicTerm(
                            location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                            symbol=Number(self.rule_count),
                        ),
                        ast.Variable(
                            location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                            name=WORLD_VARIABLE_NAME,
                        ),
                        rule.head,
                        ast.Function(
                            location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                            name="",  # For creating a tuple
                            arguments=list(collect_free_vars(rule.body)),
                            external=False,
                        ),
                    ],
                    external=False,
                ),
            )

            # Creates the new rule
            rule = ast.Rule(
                location=rule.location,
                head=xclingo_sup_literal,
                body=rule.body,
            )

        return rule


class DependenciesTransformer(GeneratorTransformer):
    def _generate_depends_rule(self, rule: ast.AST, predicate_name, dependency_catcher) -> Union[ast.AST, None]:
        dependencies = list(dependency_catcher(rule.body))
        # import pdb; pdb.set_trace()
        if len(dependencies) == 0:
            return None
        else:
            dependency_literal = ast.Literal(
                location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                sign=False,  # Positive Literal
                atom=ast.Function(
                    location=rule.body[0].location if len(rule.body) > 0 else rule.head.location,
                    name=predicate_name,
                    arguments=[
                        rule.head,
                        ast.Pool(rule.head.location, dependencies),
                    ],
                    external=False,
                ),
            )

            # Creates the new rule
            return ast.Rule(
                location=rule.location,
                head=dependency_literal,
                body=[rule.head],
            )

    def visit_Rule(self, rule: ast.AST) -> ast.AST:
        if (
            (rule.head.ast_type == ast.ASTType.Literal)
            and (rule.head.atom.ast_type == ast.ASTType.Function)
            and (rule.head.atom.name == SUPPORT_RULE_PREDICATE_NAME)
        ):  # TODO: Which expressions fall here?
            # Yield Support Rule
            yield rule
            # Yield Depends Rule (if we have dependencies)
            depends_rule = self._generate_depends_rule(rule, DEPENDS_RULE_PREDICATE_NAME, propagates)
            if depends_rule is not None:
                yield depends_rule
            # Yield Prevents Rule (if we have inhibitors)
            prevents_rule = self._generate_depends_rule(rule, PREVENTS_RULE_PREDICATE_NAME, inhibits)
            if prevents_rule is not None:
                yield prevents_rule
        else:
            yield rule
