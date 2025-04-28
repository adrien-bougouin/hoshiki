__all__ = ["convert_wav_data", "describe_transcription_result"]

from typing import Any, ByteString, TypeAlias

import numpy as np

from hoshiki._language import get_language_name_from_iso_639_1_code


WhisperAudioData: TypeAlias = np.ndarray[Any, np.dtype[np.float32]]


def convert_wav_data(wav_data: ByteString) -> WhisperAudioData:
    # https://github.com/openai/whisper/blob/517a43ecd132a2089d85f4ebc044728a71d49f6e/whisper/audio.py#L62
    #
    # https://github.com/SYSTRAN/faster-whisper/blob/1383fd4d3725bdf59c95d8834c629f45c6974981/faster_whisper/audio.py#L65
    # https://github.com/SYSTRAN/faster-whisper/blob/1383fd4d3725bdf59c95d8834c629f45c6974981/faster_whisper/audio.py#L69
    return np.frombuffer(
        wav_data, np.int16
    ).flatten().astype(np.float32) / 32768.0


def describe_transcription_result(
    result: str,
    source_language: str,
    task: str
) -> str:
    language_name = get_language_name_from_iso_639_1_code(source_language)

    return f"{task.capitalize()}d {language_name}: \"{result}\""
