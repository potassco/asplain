"""
The main entry point for the application.
"""

import sys
from pathlib import Path

from clingo import clingo_main
from dotenv import find_dotenv, load_dotenv

from .app import AsplainApp


def main() -> None:
    """
    Run the main function.
    """
    dotenv_path = Path(__package__).parent.resolve() / ".env"
    load_dotenv(dotenv_path)
    clingo_main(AsplainApp(sys.argv[0]), sys.argv[1:])
    sys.exit()


if __name__ == "__main__":
    main()
