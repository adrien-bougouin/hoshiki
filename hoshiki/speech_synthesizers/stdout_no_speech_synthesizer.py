from .speech_synthesizer import SpeechSynthesizer


class StdoutNoSpeechSynthesizer(SpeechSynthesizer):
    def say(self, something: str) -> None:
        print(f"\n--- {something}\n")
