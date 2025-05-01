__all__ = [
    "FasterWhisperBackend",
    "get",
    "OpenAIWhisperBackend",
    "WhisperBackend",
    "WhisperCPPBackend"
]

from hoshiki import Config

from .faster_whisper_backend import FasterWhisperBackend
from .openai_whisper_backend import OpenAIWhisperBackend
from .whisper_backend import WhisperBackend
from .whispercpp_backend import WhisperCPPBackend


def get(config: Config) -> WhisperBackend:
    identifier = config.get("whisper_backend", "openai-whisper")
    model_name = config.get("whisper_model", "tiny")

    match identifier:
        case "openai-whisper":
            return OpenAIWhisperBackend(
                model_name,
                fp16=config.get("openai_whisper_fp16", False)
            )
        case "faster-whisper":
            return FasterWhisperBackend(
                model_name,
                compute_type=config.get(
                    "faster_whisper_compute_type", "float32"
                )
            )
        case "whispercpp":
            if config.get("source_language") is None:
                raise ValueError(
                    f"Whisper backend '{identifier}' incompatible with"
                    " undefined source language"
                )

            return WhisperCPPBackend(model_name)
        case _:
            raise ValueError(f"unsupported Whisper backend '{identifier}'")
