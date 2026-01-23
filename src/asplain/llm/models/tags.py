"""Module for handling LLM model tags"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Tag:
    """Representation of a LLM model tag for different libraries"""

    openai: Optional[str] = None
    google: Optional[str] = None


class ModelTag(Enum):
    """Language model specifier"""

    GPT_5 = Tag(openai="gpt-5")
    GPT_5_MINI = Tag(openai="gpt-5-mini")
    GPT_5_NANO = Tag(openai="gpt-5-nano")
    GPT_4O = Tag(openai="gpt-4o")
    GPT_4O_MINI = Tag(openai="gpt-4o-mini")
    GEMINI_3_PRO = Tag(google="gemini-3-pro-preview")
    GEMINI_3_FLASH = Tag(google="gemini-3-flash-preview")
    GEMINI_2_5_FLASH = Tag(google="gemini-2.5-flash")
    GEMINI_2_FLASH = Tag(google="gemini-2.0-flash")
