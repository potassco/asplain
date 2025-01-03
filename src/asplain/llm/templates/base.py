from abc import ABC, abstractmethod


class Template(ABC):

    @abstractmethod
    def compose(self) -> str:
        """Composes the template into a string"""
