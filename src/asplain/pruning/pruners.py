import logging
from enum import Enum
from pathlib import Path
from typing import List

import clingo
from typing_extensions import Iterable

DIR_ENCODINGS = Path(__file__).parent.parent / "encodings/pruning"

log = logging.getLogger(__name__)


class PruningException(Exception):
    """Exception that is thrown when the pruning of the explanation graph malfunctions"""


class PruningMethod(Enum):
    NONE = "None"
    ORPHANS = "Orphans"


def prune_explanation_graph(symbols: Iterable[clingo.Symbol], method: PruningMethod) -> List[clingo.Symbol]:
    log.info(f"PRUNING ({method})")
    match method:
        case PruningMethod.NONE:
            return list(symbols)
        case PruningMethod.ORPHANS:
            return prune_orphans(symbols=symbols)


def prune_orphans(symbols: Iterable[clingo.Symbol]) -> List[clingo.Symbol]:
    control = clingo.Control()
    # Add explanation graph
    control.add(" ".join([f"{str(s)}." for s in symbols]))
    # Load pruning programs
    control.load(str(DIR_ENCODINGS / "orphans.lp"))
    control.load(str(DIR_ENCODINGS / "inclusion_filter.lp"))
    control.ground([("base", [])])
    with control.solve(yield_=True) as solve_handle:
        model = solve_handle.model()
        match model:
            case None:
                raise PruningException()
            case clingo.Model():
                return list(model.symbols(shown=True))
