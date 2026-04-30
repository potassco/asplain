from abc import ABC, abstractmethod


class TagProcess(ABC):
    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def tag(self) -> str:
        """The tag string to which the process function is applied"""

    @abstractmethod
    def process(self) -> None:
        """Processes"""

    def __hash__(self) -> int:
        return hash(self.tag)


class ProcessChangeRemoved(TagProcess):
    @property
    def tag(self) -> str:
        return "optional(removed)"

    def process(self) -> None:
        print("REMOVING tag optional(removed)")
