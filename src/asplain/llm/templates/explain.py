"""Basic Explanation Prompt Template"""

from pathlib import Path
from typing import Iterable, List

from .base import Template

PROMPT_FILE = "prompt_templates/explain_original.txt"


class ExplainTemplate(Template):
    """Basic Explanation Prompt Template"""

    def __init__(self, graphs: Iterable[str], answer_set: str, query: str):
        self._graphs: List[str] = list(graphs)
        self._answer_set: str = answer_set
        self._query: str = query

    def compose(self) -> str:
        graph = self._graphs[0].replace(".", "").replace("\n", "\n" + " " * 4)
        with open(Path(__file__).parent / PROMPT_FILE, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template.format(graph=graph, answer_set=self._answer_set, query=self._query)
        return prompt
