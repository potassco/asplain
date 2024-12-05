"""Module for handling LLM model tags"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class Tag:
    """Representation of a LLM model tag for different libraries"""

    huggingface: str
    ollama: str


class ModelTag(Enum):
    """Language model specifier"""

    LLAMA_3_2 = Tag(huggingface="meta-llama/Llama-3.2-3B", ollama="llama3.2:latest")
    LLAMA_3_2_1B = Tag(huggingface="meta-llama/Llama-3.2-1B", ollama="llama3.2:1b")
