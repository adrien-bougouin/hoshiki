from typing import ByteString, cast

import logging

import whisper  # type: ignore

from ._utils import convert_wav_data, describe_transcription_result
from .whisper_backend import WhisperBackend


class OpenAIWhisperBackend(WhisperBackend):
    def __init__(self, model_name: str, *, fp16: bool = False):
        self._model = whisper.load_model(model_name)
        self._fp16 = fp16

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    @property
    def sample_rate(self) -> int:
        return cast(int, whisper.audio.SAMPLE_RATE)

    def transcribe(
        self,
        wav_data: ByteString,
        *,
        language: str | None,
        task: str = "transcribe"
    ) -> tuple[str, str]:
        transcription_data = self._model.transcribe(
            convert_wav_data(wav_data),
            task=task,
            language=language,
            fp16=self._fp16
        )

        source_language = transcription_data["language"]
        transcription = transcription_data["text"]

        self._logger.info(
            describe_transcription_result(transcription, source_language, task)
        )

        return (source_language, transcription)
