"""Large Explanation Prompt Template"""

from pathlib import Path

from .base import Template

PROMPT_FILE = "prompt_templates/explain_gpt.txt"

from jinja2 import Template as JinjaTemplate

from ...utils.logging import get_logger

log = get_logger("main")


class ExplainLargeTemplate(Template):
    """Large Explanation Prompt Template"""

    def __init__(self, graph: str, predicates: str):
        self._graph: str = graph
        self._predicates: str = predicates

    def compose(self) -> str:
        graph = self._graph.replace(".", "").replace("\n", "\n" + " " * 4)
        with open(Path(__file__).parent / PROMPT_FILE, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        jinja_template = JinjaTemplate(prompt_template)
        prompt = jinja_template.render(graph=graph, predicates=self._predicates)
        log.debug("Prompt: %s", prompt)
        return prompt
