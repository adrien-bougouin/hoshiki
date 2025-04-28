from abc import ABC, abstractmethod


class Interpreter(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self, timeout: float | None) -> None:
        pass
