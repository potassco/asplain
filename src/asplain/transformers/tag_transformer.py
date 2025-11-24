from clingo import ast as _ast
from clingo import parse_term


class TagTransformer(_ast.Transformer):
    """
    Transforms the rules by adding a theory atom &tag_rule(rule_type) to the body of each rule.
    The rule_type can be one of "rule", "fact", or "constraint". It is determined based on the structure of the rule.
    """

    def visit_Rule(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        """ """
        # It is considered fact if it has no body, but for this we also ignore bodies made out only of theory atoms
        is_fact = node.head.ast_type == _ast.ASTType.Literal
        is_fact = is_fact and all(
            literal.atom.ast_type == _ast.ASTType.TheoryAtom
            and literal.atom.term.ast_type == _ast.ASTType.Function
            and literal.atom.term.name == "tag_rule"
            for literal in node.body
        )

        is_constraint = (
            node.head.ast_type == _ast.ASTType.Literal
            and node.head.atom.ast_type == _ast.ASTType.BooleanConstant
            and not node.head.atom.value
        )

        rule_type = "rule"
        if is_fact:
            rule_type = "fact"

        if is_constraint:
            rule_type = "constraint"

        theory_tag = _ast.TheoryAtom(
            location=node.location,
            term=_ast.Function(node.location, "tag_rule", [], False),
            elements=[
                _ast.TheoryAtomElement(
                    [_ast.SymbolicTerm(node.location, parse_term(rule_type))],
                    condition=[],
                )
            ],
            guard=None,
        )

        body_literal = _ast.Literal(location=node.location, sign=_ast.Sign.NoSign, atom=theory_tag)

        node.body.insert(len(node.body), body_literal)
        return node.update(**self.visit_children(node))
