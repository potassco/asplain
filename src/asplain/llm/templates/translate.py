"""NL Translation Prompt Template"""

import logging
import json
from pathlib import Path
from .base import Template

PROMPT_FILE_INSTRUCTIONS = "prompt_templates/translate_instructions.txt"
PROMPT_FILE_INPUT = "prompt_templates/translate_input.txt"

log = logging.getLogger(__name__)


class TranslateTemplate(Template):
    """NL Translation Prompt Template"""

    def __init__(self, nl_query: str, atoms: list):
        super().__init__()
        self._nl_query = nl_query
        self._atoms = atoms

    def compose_instructions(self) -> str:
        with open(Path(__file__).parent / PROMPT_FILE_INSTRUCTIONS, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template
        return prompt

    def compose_input(self) -> str:
        with open(Path(__file__).parent / PROMPT_FILE_INPUT, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template.format(query=self._nl_query, atoms=json.dumps(self._atoms, indent=2))
        return prompt
