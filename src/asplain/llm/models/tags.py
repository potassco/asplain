"""Module for handling LLM model tags"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Tag:
    """Representation of a LLM model tag for different libraries"""

    huggingface: Optional[str] = None
    ollama: Optional[str] = None


class ModelTag(Enum):
    """Language model specifier"""

    LLAMA_3_2 = Tag(huggingface="meta-llama/Llama-3.2-3B", ollama="llama3.2:latest")
    LLAMA_3_2_1B = Tag(huggingface="meta-llama/Llama-3.2-1B", ollama="llama3.2:1b")
    LLAMA_3_3 = Tag(ollama="llama3.3:latest")
