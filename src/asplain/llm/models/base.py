"""Abstract base language model wrapper"""

from abc import ABC, abstractmethod


class AbstractModel(ABC):
    """Abstract base class for all language model wrappers"""

    @abstractmethod
    def prompt(self, input_string: str) -> str:
        """prompts the language model with the given input string"""
