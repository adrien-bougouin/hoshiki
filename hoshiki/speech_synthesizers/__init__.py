__all__ = ["get", "SpeechSynthesizer", "DarwinSpeechSynthesizer"]

from hoshiki import Config
from hoshiki._audio_io import get_default_speaker_name

from .darwin_speech_synthesizer import DarwinSpeechSynthesizer
from .speech_synthesizer import SpeechSynthesizer
from .stdout_no_speech_synthesizer import StdoutNoSpeechSynthesizer


def get(config: Config) -> SpeechSynthesizer:
    identifier = config.get("speech_synthesizer", "stdout")

    match identifier:
        case "stdout":
            return StdoutNoSpeechSynthesizer()
        case "darwin":
            return DarwinSpeechSynthesizer(
                config.get("output_device", get_default_speaker_name())
            )
        case _:
            raise ValueError(f"unsupported speech synthesizer '{identifier}'")
