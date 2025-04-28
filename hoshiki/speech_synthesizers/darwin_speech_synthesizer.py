import logging
import os

from .speech_synthesizer import SpeechSynthesizer


class DarwinSpeechSynthesizer(SpeechSynthesizer):
    def __init__(self, speaker_name: str) -> None:
        self._speaker_name = speaker_name

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def say(self, something: str) -> None:
        self._logger.info(
            "Saying \"%s\" at %s.", something, self._speaker_name
        )

        os.system(f"say \"{something}\" -a \"{self._speaker_name}\"")
