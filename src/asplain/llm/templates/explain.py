"""Basic Explanation Prompt Template"""

from pathlib import Path

from .base import Template
from ..utils.graph import graph_program_to_json

PROMPT_FILE_INSTRUCTIONS = "prompt_templates/explain_instructions.txt"
PROMPT_FILE_INPUT = "prompt_templates/explain_input.txt"


class ExplainTemplate(Template):
    """Basic Explanation Prompt Template"""

    def __init__(self, contrastive_program_graph: str, query_program: str):
        super().__init__()
        self._contrastive_program_graph = contrastive_program_graph
        self._query_program = query_program

        graph_json = graph_program_to_json(self._contrastive_program_graph)
        print("JSON", graph_json.json())

    def compose_instructions(self) -> str:
        with open(Path(__file__).parent / PROMPT_FILE_INSTRUCTIONS, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template
        return prompt

    def compose_input(self) -> str:
        with open(Path(__file__).parent / PROMPT_FILE_INPUT, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template.format()
        return prompt
