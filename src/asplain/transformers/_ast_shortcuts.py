"""
A set of helper functions for working with ASTs.
"""

from typing import Generator, Sequence

from clingo.ast import (
    AST,
    ASTType,
    Sign,
    Location,
    Position,
    Variable,
)


def collect_vars_from_ast_sequence(ast_sequence: Sequence[AST]) -> list[str]:
    """
    Given a sequence of AST elements, returns a list of the variables used on them. It recursively goes into nested
    ASTs.
    """
    var_list = []
    for ast_element in ast_sequence:
        if ast_element.ast_type == ASTType.Variable:
            var_list.append(str(ast_element.name))
        elif ast_element.ast_type == ASTType.Function:
            var_list = var_list + collect_vars_from_ast_sequence(ast_element.arguments)
        elif ast_element.ast_type == ASTType.UnaryOperation:
            var_list = var_list + collect_vars_from_ast_sequence(ast_element.argument.arguments)
    return var_list


def collect_vars_from_literal(lit: AST) -> Generator[str, None, None]:
    """
    Returns of the variables used in the given literal. It handles different types of literals.
    """
    arguments = []
    if lit.ast_type == ASTType.Literal:
        if lit.atom.ast_type == ASTType.UnaryOperation:
            arguments = lit.atom.argument.arguments
        elif lit.atom.ast_type == ASTType.SymbolicAtom:
            arguments = lit.atom.symbol.arguments
        elif lit.atom.ast_type == ASTType.Function:
            arguments = lit.atom.arguments

    yield from collect_vars_from_ast_sequence(arguments)


def collect_free_vars(lit_list: Sequence[AST], ignored_predicates: list[str]) -> Generator[AST, None, None]:
    """
    Takes a literal list `lit_list` (e.g. the body of a rule) and yields a list of the free variables on it.
    """
    seen_vars, unsafe_vars = set(), set()
    for lit in lit_list:
        # ignore if its is an ignored predicate
        if lit.atom.ast_type == ASTType.Function:
            if lit.atom.name in ignored_predicates:
                continue

        # handle conditional literals
        if lit.ast_type == ASTType.ConditionalLiteral:
            for var_name in collect_vars_from_literal(lit.literal):
                unsafe_vars.add(var_name)
            continue

        if lit.atom.ast_type == ASTType.BodyAggregate:
            if lit.atom.left_guard is not None and lit.atom.left_guard.term.ast_type == ASTType.Variable:
                seen_vars.add(str(lit.atom.left_guard.term.name))
            if lit.atom.right_guard is not None and lit.atom.right_guard.term.ast_type == ASTType.Variable:
                seen_vars.add(str(lit.atom.right_guard.term.name))

        # Skip negative literals
        elif lit.sign != Sign.NoSign:
            continue

        # Handle positive body literals
        elif lit.atom.ast_type in (ASTType.SymbolicAtom, ASTType.Function):
            for var_name in collect_vars_from_literal(lit):
                seen_vars.add(var_name)
            continue

    for var_name in seen_vars:
        if var_name not in unsafe_vars:
            loc = Location(
                Position("", 0, 0),
                Position("", 0, 0),
            )
            yield Variable(loc, var_name)


def propagates(lit_list: Sequence[AST]) -> Generator[AST, None, None]:
    """
    Captures the part of a body that propagate causes.
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


def inhibits(lit_list: Sequence[AST]) -> Generator[AST, None, None]:
    """
    Captures the part of a body that do not propagate cause.
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
