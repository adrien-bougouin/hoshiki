__all__ = [
    "get",
    "SpeechRecognizer"
]

from hoshiki import Config
from hoshiki._audio_io import get_default_microphone_name

from .speech_recognizer import SpeechRecognizer


def get(config: Config) -> SpeechRecognizer:
    return SpeechRecognizer(
        config.get("input_device", get_default_microphone_name()),
        config["sample_rate"]
    )
