"""
The command line parser for the project.
"""

from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from importlib import metadata
from textwrap import dedent
from typing import Any, Optional, cast

from . import logging

__all__ = ["get_parser"]

VERSION = metadata.version("asplain")


def get_parser() -> ArgumentParser:
    """
    Return the parser for command line options.
    """
    parser = ArgumentParser(
        prog="clebug",
        description=dedent(
            """
             ▗▄▖   ▗▄▄▖ ▗▄▄▖  ▗▖     ▗▄▖  ▗▄▄▄▖ ▗▖  ▗▖
            ▐▌ ▐▌ ▐▌    ▐▌ ▐▌ ▐▌    ▐▌ ▐▌   █   ▐▛▚▖▐▌
            ▐▛▀▜▌  ▝▀▚▖ ▐▛▀▘  ▐▌    ▐▛▀▜▌   █   ▐▌ ▝▜▌
            ▐▌ ▐▌ ▗▄▄▞▘ ▐▌    ▐▙▄▄▖ ▐▌ ▐▌ ▗▄█▄▖ ▐▌  ▐▌

            Contrastive explanations for ASP using clingo.
            """,
        ),
        formatter_class=RawTextHelpFormatter,
    )
    levels = [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ]

    def get(levels: list[tuple[str, int]], name: str) -> Optional[int]:
        for key, val in levels:
            if key == name:
                return val
        return None  # nocoverage

    parser.add_argument(
        "--log",
        default="warning",
        choices=[val for _, val in levels],
        metavar=f"{{{','.join(key for key, _ in levels)}}}",
        help="set log level [%(default)s]",
        type=cast(Any, lambda name: get(levels, name)),
    )

    parser.add_argument(
        "files",
        type=FileType("r"),
        help=dedent(
            """\
            - Files containing facts that define the graph.
              See the allowed syntax: https://clingraph.readthedocs.io/en/latest/clingraph/syntax.html.

            - A single JSON file using clingos output option `--outf=2`.
            In this case, the facts defining the graphs will be loaded from each stable model."""
        ),
        nargs="*",
    )
    parser.add_argument(
        "--explanation-config",
        help=dedent(
            """\
            An encoding that defines the configuration for the
            contrastive explanation: real model, abducibles, query and distance"""
        ),
        type=FileType("r"),
        nargs="*",
        metavar="",
    )

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")
    return parser
