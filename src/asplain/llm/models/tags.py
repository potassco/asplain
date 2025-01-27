"""Module for handling LLM model tags"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Tag:
    """Representation of a LLM model tag for different libraries"""

    huggingface: Optional[str] = None
    ollama: Optional[str] = None
    openai: Optional[str] = None


class ModelTag(Enum):
    """Language model specifier"""

    LLAMA_3_2 = Tag(huggingface="meta-llama/Llama-3.2-3B", ollama="llama3.2:latest")
    LLAMA_3_2_1B = Tag(huggingface="meta-llama/Llama-3.2-1B", ollama="llama3.2:1b")
    LLAMA_3_3 = Tag(ollama="llama3.3:latest")
    DEEPSEEK_R1_1B = Tag(ollama="deepseek-r1:1.5b")
    DEEPSEEK_R1_7B = Tag(ollama="deepseek-r1:7b")
    DEEPSEEK_R1_8B = Tag(ollama="deepseek-r1:8b")
    DEEPSEEK_R1_14B = Tag(ollama="deepseek-r1:14b")
    DEEPSEEK_R1_32B = Tag(ollama="deepseek-r1:32b")
    DEEPSEEK_R1_70B = Tag(ollama="deepseek-r1:70b")
    GPT_4O = Tag(openai="gpt-4o")
    GPT_4O_MINI = Tag(openai="gpt-4o-mini")
