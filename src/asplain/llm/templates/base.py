"""Base Prompt Template"""

from abc import ABC, abstractmethod


class Template(ABC):
    """Base Prompt Template"""

    @abstractmethod
    def compose(self) -> str:
        """Composes the template into a string"""
