from abc import ABC, abstractmethod


class SpeechSynthesizer(ABC):
    @abstractmethod
    def say(self, something: str) -> None:
        pass
