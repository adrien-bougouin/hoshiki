from typing import ByteString

import logging

import whispercpp

from ._utils import convert_wav_data, describe_transcription_result
from .whisper_backend import WhisperBackend


class WhisperCPPBackend(WhisperBackend):
    def __init__(self, model_name: str):
        self._model = whispercpp.Whisper.from_pretrained(model_name)

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    @property
    def sample_rate(self) -> int:
        return 16000

    def transcribe(
        self,
        wav_data: ByteString,
        *,
        language: str | None,
        task: str = "transcribe"
    ) -> tuple[str, str]:
        if language is None:
            raise ValueError("None 'language' is not supported")

        self._model.params.language = language
        self._model.params.translate = task == "translate"
        self._model.params.suppress_non_speech_tokens = True  # type: ignore

        transcription = self._model.transcribe(
            convert_wav_data(wav_data)
        ).strip()

        self._logger.info(
            describe_transcription_result(transcription, language, task)
        )

        return (language, transcription)
