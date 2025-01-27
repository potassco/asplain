from pathlib import Path
from typing import Iterable, List

from .base import Template

PROMPT_FILE = "prompt_templates/explain_large.txt"


class ExplainLargeTemplate(Template):

    def __init__(self, graphs: Iterable[str], predicates: str):
        self._graphs: List[str] = list(graphs)
        self._predicates: str = predicates

    def compose(self) -> str:
        graph = self._graphs[0].replace(".", "").replace("\n", "\n" + " " * 4)
        with open(Path(__file__).parent / PROMPT_FILE, "r") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template.format(graph=graph, predicates=self._predicates)
        return prompt
