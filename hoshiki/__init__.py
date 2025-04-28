__all__ = [
    "interpreters",
    "Config",
    "speech_recognizers",
    "speech_synthesizers",
    "whisper_backends"
]

from typing import Any, TypeAlias

Config: TypeAlias = dict[str, Any]
