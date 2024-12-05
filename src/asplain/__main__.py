"""
The main entry point for the application.
"""

import sys

from clingo import clingo_main

from .app import AsplainApp
from .llm.models import ModelTag, OllamaModel

TEST_LLM = True


def main() -> None:
    """
    Run the main function.
    """
    if TEST_LLM:
        model = OllamaModel(ModelTag.LLAMA_3_2_1B)
        response = model.prompt("What's 9 + 10?")
        print("LLM: ", response)
    else:
        clingo_main(AsplainApp(sys.argv[0]), sys.argv[1:])
    sys.exit()


if __name__ == "__main__":
    main()
