from typing import Sequence

from clingo import Number, String
from clingo.ast import (
    AST,
    ASTType,
    BodyAggregate,
    BodyAggregateElement,
    BooleanConstant,
    ConditionalLiteral,
    Function,
    Literal,
    Location,
    Pool,
    Position,
    Sign,
    SymbolicAtom,
    SymbolicTerm,
    Variable,
)


def collect_free_vars(lit_list: Sequence[AST], ignored_predicates=[]):
    def collect_vars(_lit: AST):
        def _collect_vars(arguments: Sequence[AST]):
            vars = []
            for arg in arguments:
                if arg.ast_type == ASTType.Variable:
                    vars.append(str(arg.name))
                elif arg.ast_type == ASTType.Function:
                    vars = vars + _collect_vars(arg.arguments)
                elif arg.ast_type == ASTType.UnaryOperation:
                    vars = vars + _collect_vars(arg.argument.arguments)
            return vars

        if _lit.ast_type == ASTType.Literal:
            if _lit.atom.ast_type == ASTType.UnaryOperation:
                arguments = _lit.atom.argument.arguments
            elif _lit.atom.ast_type == ASTType.SymbolicAtom:
                arguments = _lit.atom.symbol.arguments
            elif _lit.atom.ast_type == ASTType.Function:
                arguments = _lit.atom.arguments

            for v in _collect_vars(arguments):
                yield v

    seen_vars, unsafe_vars = set(), set()
    for lit in lit_list:
        # ignore if its is an ignored predicate
        if lit.atom.ast_type == ASTType.Function:
            if lit.atom.name in ignored_predicates:
                continue

        # handle conditional literals
        if lit.ast_type == ASTType.ConditionalLiteral:
            for var_name in collect_vars(lit.literal):
                unsafe_vars.add(var_name)
            continue

        # handle comparisons
        # if lit.atom.ast_type == ASTType.Comparison:
        #     import pdb; pdb.set_trace()
        #     for arg in lit.atom.arguments:
        #         if arg.ast_type == ASTType.Variable:
        #             seen_vars.add(str(arg))

        if lit.atom.ast_type == ASTType.BodyAggregate:
            if lit.atom.left_guard is not None and lit.atom.left_guard.term.ast_type == ASTType.Variable:
                seen_vars.add(str(lit.atom.left_guard.term.name))
            if lit.atom.right_guard is not None and lit.atom.right_guard.term.ast_type == ASTType.Variable:
                seen_vars.add(str(lit.atom.right_guard.term.name))

        # Skip negative literals
        elif lit.sign != Sign.NoSign:
            continue

        # handle positive body literals
        elif lit.atom.ast_type == ASTType.SymbolicAtom or lit.atom.ast_type == ASTType.Function:
            for var_name in collect_vars(lit):
                seen_vars.add(var_name)
            continue

    # import pdb; pdb.set_trace()

    for var_name in seen_vars:
        if var_name not in unsafe_vars:
            # TODO: to handle location properly
            loc = Location(
                Position("", 0, 0),
                Position("", 0, 0),
            )
            yield Variable(loc, var_name)


def propagates(lit_list: Sequence[AST]):
    """Captures the part of a body that propagate causes.
    This is, the positive part of the body of a rule. Comparison literals are ignored.

    Args:
        lit_list (Sequence[AST]): list of literals to be processed. Normally
        a rule's body.

    Yields:
        AST: literals that propagate cause.
    """
    for lit in lit_list:
        if (
            lit.ast_type != ASTType.ConditionalLiteral
            and lit.sign == Sign.NoSign
            and lit.atom.ast_type == ASTType.SymbolicAtom
        ):
            yield lit


def inhibits(lit_list: Sequence[AST]):
    """Captures the part of a body that do not propagate cause.
    This is, the negative part of the body of a rule. Comparison literals are ignored.

    Args:
        lit_list (Sequence[AST]): list of literals to be processed. Normally
        a rule's body.

    Yields:
        AST: literals that do not propagate cause.
    """
    for lit in lit_list:
        if (
            lit.ast_type != ASTType.ConditionalLiteral
            and lit.sign == Sign.Negation  # Negative Literals
            and lit.atom.ast_type == ASTType.SymbolicAtom
        ):
            yield lit.atom
