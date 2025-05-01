from typing import ByteString, Tuple

import logging

from hoshiki._language import \
    get_iso_639_1_language_code, get_language_name_from_iso_639_1_code
from hoshiki._threading import Repeater, Worker
from hoshiki.interpreters import Interpreter
from hoshiki.speech_recognizers import SpeechRecognizer
from hoshiki.speech_synthesizers import SpeechSynthesizer
from hoshiki.whisper_backends import WhisperBackend


class WhisperTranslateInterpreter(Interpreter):
    def __init__(
        self,
        source_language: str | None,
        language_allow_list: Tuple[str],
        speech_recognizer: SpeechRecognizer,
        speech_synthesizer: SpeechSynthesizer,
        whisper_backend: WhisperBackend
    ):
        # Supplying the input language in ISO-639-1 (e.g. en) format will
        # improve accuracy and latency.
        #
        # --https://platform.openai.com/docs/api-reference/audio/createTranscription
        self._source_language = get_iso_639_1_language_code(
            source_language
        ) if source_language is not None else source_language

        self._language_allow_list = [
            get_iso_639_1_language_code(lang) for lang in language_allow_list
        ]

        self._speech_recognizer = speech_recognizer
        self._speech_synthesizer = speech_synthesizer

        self._whisper_backend = whisper_backend
        self._whisper_task = \
            "transcribe" if self._source_language == "en" else "translate"

        self._workers: list[Repeater | Worker[ByteString] | Worker[str]] = []

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def start(self) -> None:
        if self._is_running():
            return

        speech_synthesizing_worker: Worker[str] = Worker(
            lambda text:
                self._speech_synthesizer.say(text) if text != "" else None
        )

        translation_worker: Worker[ByteString] = Worker(
            lambda wav_data: speech_synthesizing_worker.enqueue(
                self._translate_speech_to_text(wav_data)
            )
        )

        speech_recognition_worker = Repeater(
            lambda: self._speech_recognizer.listen(translation_worker.enqueue),
            interval=0
        )

        self._workers = [
            speech_recognition_worker,
            translation_worker,
            speech_synthesizing_worker
        ]

        for worker in self._workers:
            worker.start()

    def stop(self, timeout: float | None = None) -> None:
        for worker in self._workers:
            worker.stop(timeout)

        self._workers = []

    def _is_running(self) -> bool:
        return len(self._workers) > 0

    def _translate_speech_to_text(self, wav_data: ByteString) -> str:
        source_language, translation = self._whisper_backend.transcribe(
            wav_data,
            task=self._whisper_task,
            language=self._source_language
        )

        if not self._validate_source_language(source_language):
            translation = ""

            translation_type = \
                "translation" \
                if self._whisper_task == "translate" \
                else "transcription"
            language_name = get_language_name_from_iso_639_1_code(
                source_language
            )

            self._logger.info(
                "Filtered out %s for %s", translation_type, language_name
            )

        return translation

    def _validate_source_language(self, source_language: str) -> bool:
        return \
            True if not self._language_allow_list \
            else (source_language in self._language_allow_list)
