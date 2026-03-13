from enum import Enum
from typing import List

import clingo
from typing_extensions import Iterable


class PruningMethod(Enum):
    ORPHANS = "Orphans"


def prune_explanation_graph(symbols: Iterable[clingo.Symbol], method: PruningMethod) -> List[clingo.Symbol]:
    print("PRUNING", f"({method})")
    match method:
        case PruningMethod.ORPHANS:
            return prune_orphans(symbols=symbols)


def prune_orphans(symbols: Iterable[clingo.Symbol]) -> List[clingo.Symbol]:
    return list(symbols)
