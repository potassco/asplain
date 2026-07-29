"""Base Prompt Template"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar


class Template(ABC):
    """Base Prompt Template"""

    PROMPT_FILE_INSTRUCTIONS: ClassVar[str | None] = None
    PROMPT_FILE_INPUT: ClassVar[str | None] = None

    def compose_instructions(self) -> str:
        """Composes the instructions template string"""
        if self.PROMPT_FILE_INSTRUCTIONS is None:
            msg = "PROMPT_FILE_INSTRUCTIONS must be set in subclasses"
            raise ValueError(msg)

        with open(Path(__file__).parent / self.PROMPT_FILE_INSTRUCTIONS, "r", encoding="utf-8") as prompt_file:
            prompt_template = prompt_file.read()
        prompt = prompt_template
        return prompt

    @abstractmethod
    def compose_input(self) -> str:
        """Composes the input template string"""
