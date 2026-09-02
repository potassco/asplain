"""Pruning methods for the explanation graph."""

import logging
from collections.abc import Iterable, Sequence
from enum import Enum
from pathlib import Path

import clingo

DIR_ENCODINGS = Path(__file__).parent.parent / "encodings/pruning"
ENCODING_PATHS = "paths.lp"
ENCODING_PATHS_UNDIRECTED = "paths_undirected.lp"
ENCODING_ORPHANS = "orphans.lp"
ENCODING_CHANGES = "changes.lp"
ENCODING_INCLUSION_FILTER = "inclusion_filter.lp"
ENCODING_INERTIA_CONDENSATION = "inertia_condensation.lp"
SIGNATURE_PATH_DEPTH = "path_depth"

log = logging.getLogger(__name__)


class PruningException(Exception):
    """Exception that is thrown when the pruning of the explanation graph malfunctions."""


class PruningMethod(Enum):
    """Available pruning methods."""

    NONE = "None"
    ORPHANS = "Orphans"
    PATHS = "Path"
    PATHS_UNDIRECTED = "Path Undirected"
    CHANGES = "Changes"
    INERTIA_CONDENSATION = "Inertia Condensation"


def prune_sequence(
    symbols: Iterable[clingo.Symbol],
    methods: Sequence[PruningMethod],
    path_depth: int = 0,
) -> list[clingo.Symbol]:
    """Apply prunings to the explanation graph in a fixed sequence."""
    transformed = list(symbols)
    for method in methods:
        transformed = prune_explanation_graph(transformed, method=method, path_depth=path_depth)
        print([str(a) for a in transformed])
        print()
    return transformed


def prune_explanation_graph(
    symbols: Iterable[clingo.Symbol],
    method: PruningMethod,
    path_depth: int = 0,
) -> list[clingo.Symbol]:
    """Prune the explanation graph using the specified method."""
    log.info("Pruning Graph using Method: %s", method)
    match method:
        case PruningMethod.NONE:
            return list(symbols)
        case PruningMethod.ORPHANS:
            return prune_orphans(symbols=symbols)
        case PruningMethod.PATHS:
            return prune_path(symbols=symbols, depth=path_depth)
        case PruningMethod.PATHS_UNDIRECTED:
            return prune_path_undirected(symbols=symbols)
        case PruningMethod.CHANGES:
            return prune_changes(symbols=symbols)
        case PruningMethod.INERTIA_CONDENSATION:
            return prunte_inertia_condensation(symbols=symbols)


def prunte_inertia_condensation(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
    """
    Pruning method condensing inertia chains.

    Args:
        symbols: The symbols of the explanation graph to prune

    """
    symbols = list(symbols)
    return solve_program(symbols=symbols, files=[ENCODING_INERTIA_CONDENSATION, ENCODING_INCLUSION_FILTER])


def prune_changes(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
    """
    Prune methods to keep only changes between reference and foil models.

    Args:
        symbols: The symbols of the explanation graph to prune
    """
    return solve_program(symbols=symbols, files=[ENCODING_CHANGES, ENCODING_INCLUSION_FILTER])


def prune_orphans(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
    """
    Prune method to remove orphan nodes, i.e., nodes that are not connected to any query.

    Args:
        symbols: The symbols of the explanation graph to prune
    """
    return solve_program(symbols=symbols, files=[ENCODING_ORPHANS, ENCODING_INCLUSION_FILTER])


def prune_path(symbols: Iterable[clingo.Symbol], depth: int = 0) -> list[clingo.Symbol]:
    """
    Pruning method finding a connecting path between changed rules and query in the graph with a maximum depth.

    Args:
        symbols: The symbols of the explanation graph to prune
        depth: The maximum depth of the path to keep
    """
    symbols = list(symbols)
    # Add depth symbol
    depth_symbol = clingo.parse_term(f"{SIGNATURE_PATH_DEPTH}({depth})")
    symbols.append(depth_symbol)
    # Solve and return model
    return solve_program(symbols=symbols, files=[ENCODING_PATHS, ENCODING_INCLUSION_FILTER])


def prune_path_undirected(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
    """
    Pruning method finding a connecting path between changed rules and query in the graph disregarding edge directions.

    Args:
        symbols: The symbols of the explanation graph to prune

    """
    symbols = list(symbols)
    return solve_program(symbols=symbols, files=[ENCODING_PATHS_UNDIRECTED, ENCODING_INCLUSION_FILTER])


def solve_program(symbols: Iterable[clingo.Symbol], files: Iterable[str]) -> list[clingo.Symbol]:
    """
    Solve the ASP program with the given symbols and files.

    Args:
        symbols: The symbols of the explanation graph to include in the program
        files: The ASP files to load and include in the program

    Returns:
        The symbols of the solved model
    """
    control = clingo.Control()
    # Add explanation graph
    control.add(" ".join([f"{str(s)}." for s in symbols]))
    # Load pruning programs
    for file in files:
        control.load(str(DIR_ENCODINGS / file))
    control.ground([("base", [])])
    with control.solve(yield_=True) as solve_handle:
        model = solve_handle.model()
        match model:
            case None:
                raise PruningException()
            case clingo.Model():
                return list(model.symbols(shown=True))
    raise PruningException()
