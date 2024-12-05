"""Abstract base language model wrapper"""

from abc import ABC, abstractmethod

from . import ModelTag


class AbstractModel(ABC):
    """Abstract base class for all language model wrappers"""

    @property
    @abstractmethod
    def model_tag_key(self) -> str:
        """Key to access the model tag from a ModelTag object"""

    def __init__(self, model_tag: ModelTag) -> None:
        """Abstract constructor"""
        self.model_tag: str = getattr(model_tag.value, self.model_tag_key)

    @abstractmethod
    def prompt(self, input_string: str) -> str:
        """Prompts the language model with the given input string"""
