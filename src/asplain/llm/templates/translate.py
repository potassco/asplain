"""NL Translation Prompt Template"""

import json
import logging
from pathlib import Path
from typing import Any

from .base import Template

log = logging.getLogger(__name__)


class TranslateTemplate(Template):
    """NL Translation Prompt Template"""

    PROMPT_FILE_INSTRUCTIONS = "prompt_templates/translate_instructions.txt"
    PROMPT_FILE_INPUT = "prompt_templates/translate_input.txt"

    def __init__(self, nl_query: str, atoms: list[Any]):
        super().__init__()
        self._nl_query = nl_query
        self._atoms = atoms

    def compose_input(self) -> str:
        with open(Path(__file__).parent / self.PROMPT_FILE_INPUT, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template.format(query=self._nl_query, atoms=json.dumps(self._atoms, indent=2))
        return prompt
