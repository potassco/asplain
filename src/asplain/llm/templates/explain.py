"""Basic Explanation Prompt Template"""

import logging
from pathlib import Path

from ..utils import Graph
from .base import Template

log = logging.getLogger(__name__)


class ExplainTemplate(Template):
    """Basic Explanation Prompt Template"""

    PROMPT_FILE_INSTRUCTIONS = "prompt_templates/explain_instructions.txt"
    PROMPT_FILE_INPUT = "prompt_templates/explain_input.txt"

    def __init__(self, contrastive_program_graph: str):
        super().__init__()
        self._contrastive_program_graph = contrastive_program_graph
        self._graph = Graph(self._contrastive_program_graph)

    def compose_input(self) -> str:
        with open(Path(__file__).parent / self.PROMPT_FILE_INPUT, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template.format(graph=self._graph.json)
        log.debug("-----------------\nLLM Prompt Input:\n%s", prompt)
        log.debug(prompt)
        return prompt
