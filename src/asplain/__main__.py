"""
The main entry point for the application.
"""

import sys

from clingo import clingo_main

from asplain.app import AsplainApp

from .utils.clingo import parse_constants
from .utils.logging import configure_logging, get_logger
from .utils.parser import get_parser


def main() -> None:
    """
    Run the main function.
    """
    constants = parse_constants(sys.argv[2:])
    clingo_main(AsplainApp(sys.argv[0], constants=constants), sys.argv[1:])
    sys.exit()


if __name__ == "__main__":
    main()
