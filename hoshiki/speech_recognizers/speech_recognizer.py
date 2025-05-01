from typing import ByteString, Callable

import logging
import sys

import speech_recognition as sr  # type: ignore

from hoshiki._audio_io import get_microphone_index_from_name


class SpeechRecognizer:
    def __init__(self, microphone_name: str, sample_rate: int) -> None:

        self._microphone: sr.Microphone = sr.Microphone(
            device_index=get_microphone_index_from_name(microphone_name),
            sample_rate=sample_rate
        )

        self._recognizer: sr.Recognizer = sr.Recognizer()

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def listen(self, callback: Callable[[ByteString], None]) -> None:
        try:
            with self._microphone:
                audio: sr.AudioData = self._recognizer.listen(self._microphone)
        except sr.WaitTimeoutError:
            pass
        else:
            audio_duration: float = \
                (sys.getsizeof(audio.frame_data) / audio.sample_width) \
                / audio.sample_rate

            self._logger.info(
                "Detected %.3f seconds of speech", audio_duration
            )

            if audio_duration > 0:
                callback(audio.get_wav_data())
