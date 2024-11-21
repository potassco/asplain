"""
The asplain project.
"""

import logging
import os

from importlib.resources import path


from clingo import Control
from clingo.script import enable_python
from clingraph.clingo_utils import ClingraphContext  # type: ignore
from clingraph.graphviz import compute_graphs, render  # type: ignore
from clingraph.orm import Factbase  # type: ignore

from .utils.logging import get_logger

log = get_logger("main")


def viz_explanation(explanation_symbols, directory="out", name_format="explanation.png"):
    """
    Visualize explanation using clingraph

    Args:
        explanation_symbols (List): _description_
    """
    fb = Factbase(default_graph="trace")
    ctl = Control(["--warn=none"])
    ctx = ClingraphContext()
    ctl.add("base", [], "\n".join([s + "." for s in explanation_symbols]))
    with path("asplain.encodings", "clingraph.lp") as clingraph_encoding:
        ctl.load(str(clingraph_encoding))
    enable_python()
    ctl.ground([("base", [])], context=ctx)
    ctl.solve(on_model=fb.add_model)
    graphs = compute_graphs(fb)
    files = render(graphs, view=True, directory=directory, name_format=name_format)
    log.info("Render saved in %s", files["trace"])
