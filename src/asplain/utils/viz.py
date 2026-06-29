"""Visualization utilities for Asplain."""

import logging
from typing import Any

from clingo import Control
from clingo.script import enable_python
from clingraph.clingo_utils import ClingraphContext  # type: ignore
from clingraph.graphviz import compute_graphs, render  # type: ignore
from clingraph.orm import Factbase  # type: ignore

from asplain.utils.clingo import load_encoding

log = logging.getLogger(__name__)


def viz_graph(
    pg: str,
    title: str,
    show: bool = False,
    name: str = "graph",
    format: str = "png",  # pylint: disable=redefined-builtin
) -> dict[str, Any]:
    """
    Visualize the explanation graph using cligraph
    Args:
        pg: The program graph as a string of facts. This might define multiple graphs.
        title: Title of the graph.
        open: Whether to open the generated graph image.
        name: Name format for the output file.
    """
    dpi = 500 if format == "png" else 80
    fb = Factbase(prefix="v")
    ctl = Control(["--warn=none", "--const", f"setdpi={dpi}"])
    ctx = ClingraphContext()
    ctl.add("base", [], pg)
    ctl.add("base", [], f'title("{title}").')
    load_encoding(ctl, "viz-pg.lp")
    enable_python()
    ctl.ground([("base", [])], context=ctx)
    ctl.solve(on_model=fb.add_model)
    graphs = compute_graphs(fb, graphviz_type="directed")
    files = render(graphs, view=show, directory="out", name_format=f"{name}", format=format)
    if len(files) == 0:
        log.warning("No graph images were rendered.")
        return graphs  # type: ignore
    log.info("Graph image saved in: %s", files["default"])
    return graphs  # type: ignore
