__all__ = ["WhisperBackend"]

from typing import ByteString

from abc import ABC, abstractmethod


class WhisperBackend(ABC):
    @property
    @abstractmethod
    def sample_rate(self) -> int:
        pass

    @abstractmethod
    def transcribe(
        self,
        wav_data: ByteString,
        *,
        language: str | None,
        task: str = "transcribe"
    ) -> tuple[str, str]:
        pass
