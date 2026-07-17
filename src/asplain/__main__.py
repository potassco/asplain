"""
The main entry point for the application.
"""

import os
import subprocess
import sys
from typing import Sequence

from clingo import clingo_main

from asplain.app import AsplainApp

from .utils.clingo import parse_constants

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = os.path.join(MAIN_PATH, "ui")
ENCODINGS_PATH = os.path.join(MAIN_PATH, "encodings")


def clinguin_command(args: Sequence[str]) -> Sequence[str]:  # nocoverage
    """
    Generate the clinguin command for the system. With the given reified input.

    Args:
        args: the argument list from the command line
    Returns:
        str: The clinguin command to be executed.
    """

    command = ["clinguin", "client-server"]
    command += ["--ui-files", os.path.join(ENCODINGS_PATH, "ui.lp")]
    command += ["--custom-classes", UI_PATH]
    command += ["--backend", "ASPlainBackend"]
    command += ["--domain-files"]
    command += args
    return command


def main() -> None:
    """
    Run the main function.
    """
    if sys.argv[1] == "ui":  # nocoverage
        print("Running in user interface mode. Use Ctrl+C to exit.")
        command = clinguin_command(sys.argv[2:])
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, shell=False, check=False)
        if result.returncode != 0:
            print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

    constants = parse_constants(sys.argv[2:])
    clingo_main(AsplainApp(sys.argv[0], constants=constants), sys.argv[1:])
    sys.exit()


if __name__ == "__main__":
    main()
