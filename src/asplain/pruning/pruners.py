import logging
from enum import Enum
from pathlib import Path
from typing import List

import clingo
from typing_extensions import Iterable

DIR_ENCODINGS = Path(__file__).parent.parent / "encodings/pruning"
ENCODING_PATHS = "paths.lp"
ENCODING_ORPHANS = "orphans.lp"
ENCODING_CHANGES = "changes.lp"
ENCODING_INCLUSION_FILTER = "inclusion_filter.lp"
SIGNATURE_PATH_DEPTH = "path_depth"

log = logging.getLogger(__name__)


class PruningException(Exception):
    """Exception that is thrown when the pruning of the explanation graph malfunctions"""


class PruningMethod(Enum):
    NONE = "None"
    ORPHANS = "Orphans"
    PATHS = "Path"
    CHANGES = "Changes"


def prune_explanation_graph(
    symbols: Iterable[clingo.Symbol],
    method: PruningMethod,
    path_depth: int = 0,
) -> List[clingo.Symbol]:
    log.info(f"Pruning Graph using Method: {method}")
    match method:
        case PruningMethod.NONE:
            return list(symbols)
        case PruningMethod.ORPHANS:
            return prune_orphans(symbols=symbols)
        case PruningMethod.PATHS:
            return prune_path(symbols=symbols, depth=path_depth)
        case PruningMethod.CHANGES:
            return prune_changes(symbols=symbols)


def prune_changes(symbols: Iterable[clingo.Symbol]) -> List[clingo.Symbol]:
    return solve_program(symbols=symbols, files=[ENCODING_CHANGES, ENCODING_INCLUSION_FILTER])


def prune_orphans(symbols: Iterable[clingo.Symbol]) -> List[clingo.Symbol]:
    return solve_program(symbols=symbols, files=[ENCODING_ORPHANS, ENCODING_INCLUSION_FILTER])


def prune_path(symbols: Iterable[clingo.Symbol], depth: int = 0) -> List[clingo.Symbol]:
    symbols = list(symbols)
    # Add depth symbol
    depth_symbol = clingo.parse_term(f"{SIGNATURE_PATH_DEPTH}({depth})")
    symbols.append(depth_symbol)
    # Solve and return model
    return solve_program(symbols=symbols, files=[ENCODING_PATHS, ENCODING_INCLUSION_FILTER])


def solve_program(symbols: Iterable[clingo.Symbol], files: Iterable[str]) -> List[clingo.Symbol]:
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
