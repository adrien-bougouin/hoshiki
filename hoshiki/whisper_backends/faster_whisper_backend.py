from typing import ByteString

import logging

import faster_whisper  # type: ignore

from ._utils import convert_wav_data, describe_transcription_result
from .whisper_backend import WhisperBackend


class FasterWhisperBackend(WhisperBackend):
    def __init__(self, model_name: str, *, compute_type: str = "float32"):
        self._model = faster_whisper.WhisperModel(
            model_name,
            compute_type=compute_type
        )

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
        transcription_data = self._model.transcribe(
            convert_wav_data(wav_data),
            task=task,
            language=language
        )

        source_language = transcription_data[1].language
        transcription = " ".join(
            [td.text for td in list(transcription_data[0])]
        ).strip()

        self._logger.info(
            describe_transcription_result(transcription, source_language, task)
        )

        return (source_language, transcription)
