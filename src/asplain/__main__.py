"""
The main entry point for the application.
"""

import sys

from clingo import clingo_main
from dotenv import load_dotenv

from .app import AsplainApp


def main() -> None:
    """
    Run the main function.
    """
    load_dotenv()
    clingo_main(AsplainApp(sys.argv[0]), sys.argv[1:])
    sys.exit()


if __name__ == "__main__":
    main()
