from abc import ABC, abstractmethod


class AbstractModel(ABC):

    @abstractmethod
    def prompt(self, input_string: str) -> str:
        pass
