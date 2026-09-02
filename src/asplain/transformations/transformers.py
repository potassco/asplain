"""Transformation methods for the explanation graph."""

import logging
from collections.abc import Iterable, Sequence
from enum import Enum
from pathlib import Path

import clingo

DIR_ENCODINGS = Path(__file__).parent.parent / "encodings/transformations"
ENCODING_PATHS = "paths.lp"
ENCODING_PATHS_UNDIRECTED = "paths_undirected.lp"
ENCODING_ORPHANS = "orphans.lp"
ENCODING_CHANGES = "changes.lp"
ENCODING_INCLUSION_FILTER = "inclusion_filter.lp"
ENCODING_INERTIA_CONDENSATION = "inertia_condensation.lp"
SIGNATURE_PATH_DEPTH = "path_depth"

log = logging.getLogger(__name__)


class TransformationException(Exception):
    """Exception that is thrown when the transformation of the explanation graph malfunctions."""


class TransformationMethod(Enum):
    """Available transformation methods."""

    NONE = "None"
    ORPHANS = "Orphans"
    PATHS = "Path"
    PATHS_UNDIRECTED = "Path Undirected"
    CHANGES = "Changes"
    INERTIA_CONDENSATION = "Inertia Condensation"


def apply_transformation_sequence(
    symbols: Iterable[clingo.Symbol],
    methods: Sequence[TransformationMethod],
    path_depth: int = 0,
) -> list[clingo.Symbol]:
    """Apply transformations to the explanation graph in a fixed sequence."""
    transformed = list(symbols)
    for method in methods:
        transformed = apply_transformation(transformed, method=method, path_depth=path_depth)
        print([str(a) for a in transformed])
        print()
    return transformed


def apply_transformation(
    symbols: Iterable[clingo.Symbol],
    method: TransformationMethod,
    path_depth: int = 0,
) -> list[clingo.Symbol]:
    """Transform the explanation graph using the specified method."""
    log.info("Transforming Graph using Method: %s", method)
    match method:
        case TransformationMethod.NONE:
            return list(symbols)
        case TransformationMethod.ORPHANS:
            return transform_orphans(symbols=symbols)
        case TransformationMethod.PATHS:
            return transform_path(symbols=symbols, depth=path_depth)
        case TransformationMethod.PATHS_UNDIRECTED:
            return transform_path_undirected(symbols=symbols)
        case TransformationMethod.CHANGES:
            return transform_changes(symbols=symbols)
        case TransformationMethod.INERTIA_CONDENSATION:
            return transform_inertia_condensation(symbols=symbols)


def transform_inertia_condensation(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
    """
    Transform the explanation graph by condensing inertia chains.

    Args:
        symbols: The symbols of the explanation graph to prune

    """
    symbols = list(symbols)
    return solve_program(symbols=symbols, files=[ENCODING_INERTIA_CONDENSATION, ENCODING_INCLUSION_FILTER])


def transform_changes(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
    """
    Prune methods to keep only changes between reference and foil models.

    Args:
        symbols: The symbols of the explanation graph to prune
    """
    return solve_program(symbols=symbols, files=[ENCODING_CHANGES, ENCODING_INCLUSION_FILTER])


def transform_orphans(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
    """
    Prune method to remove orphan nodes, i.e., nodes that are not connected to any query.

    Args:
        symbols: The symbols of the explanation graph to prune
    """
    return solve_program(symbols=symbols, files=[ENCODING_ORPHANS, ENCODING_INCLUSION_FILTER])


def transform_path(symbols: Iterable[clingo.Symbol], depth: int = 0) -> list[clingo.Symbol]:
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


def transform_path_undirected(symbols: Iterable[clingo.Symbol]) -> list[clingo.Symbol]:
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
                raise TransformationException()
            case clingo.Model():
                return list(model.symbols(shown=True))
    raise TransformationException()
