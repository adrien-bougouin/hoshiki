__all__ = [
    "get",
    "Interpreter",
    "WhisperTranslateInterpreter"
]

from hoshiki import \
    Config, speech_recognizers, speech_synthesizers, whisper_backends

from .interpreter import Interpreter
from .whisper_translate_interpreter import WhisperTranslateInterpreter


def get(config: Config) -> Interpreter:
    identifier = config.get("interpreter", "whisper-translate")

    match identifier:
        case "whisper-translate":
            whisper_backend = whisper_backends.get(config)
            recommended_sample_rate = whisper_backend.sample_rate

            return WhisperTranslateInterpreter(
                config["source_language"],
                config.get("only", ()),
                speech_recognizers.get({
                    "sample_rate": recommended_sample_rate,
                    **config
                }),
                speech_synthesizers.get(config),
                whisper_backend
            )
        case _:
            raise ValueError(f"unsupported interpreter '{identifier}'")
