# Hoshiki

Consecutive Any-to-English interpreter.

> Hoshi Sato [..] is a fictional character in the science fiction television series Star Trek: Enterprise. [...] She is an acknowledged linguistic genius and expert at operating the universal translator, a key instrument in allowing the crew to communicate with alien cultures.
>
> --https://en.wikipedia.org/wiki/Hoshi_Sato

> In Japanese, the character 機 (ki) means "machine," "device," or "mechanism."
>
> --https://jisho.org/search/%E6%A9%9F

## Getting started

### Setup
```bash
make dependencies
```

### Run
```bash
make run ARGS="ja --whisper-backend faster-whisper --faster-whisper-compute-type int8"
```

### Show help
```bash
make run ARGS="--help"
Usage: pipenv run python -m hoshiki [OPTIONS] [SOURCE_LANGUAGE]

  Consecutive Any-to-English interpreter.

Options:
  --interpreter [whisper-translate]
                                  Name of the interpreter to use.  [default:
                                  whisper-translate]
  --speech-synthesizer [stdout|darwin]
                                  Name of the speech synthesizer to use.
                                  [default: stdout]
  --only LANGUAGE                 Selects which source language to transcribe.
                                  Only works when SOURCE_LANGUAGE is not
                                  provided (and language is automatically
                                  detected).
  --input-device MICROPHONE_NAME  Name of the microphone device to record from
                                  (e.g. "MacBook Pro Microphone"). List
                                  available devices with '--input-device ?'.
  --output-device SPEAKER_NAME    Name of the speaker device to speak into
                                  (e.g. "MacBook Pro Speakers"). List
                                  available devices with '--output-device ?'.
  --whisper-model MODEL_NAME      Name of the whisper model to use. Option
                                  available for the whisper-translate
                                  interpreter, the openai-whisper backend, and
                                  the faster-whisper backend.  [default: base]
  --whisper-backend [openai-whisper|faster-whisper]
                                  Whisper backend to use. Option available for
                                  the whisper-translate interpreter.
                                  [default: openai-whisper]
  --openai-whisper-fp16           Use half-precision floating point numbers
                                  (instead of full-precision), for faster and
                                  more memory efficient speech-to-text
                                  processing with the openai-whisper backend
                                  with GPU.
  --faster-whisper-compute-type [int8|int8_float32|int8_float16|int8_bfloat16|int16|float16|bfloat16|float32]
                                  Numerical precision, for better managing the
                                  speed and the memory usage of the speech-to-
                                  text processing with the faster-whisper
                                  backend.  [default: float32]
  -v, --verbose                   Print operation details.
  -d, --debug                     Print internal operation details.
  --help                          Show this message and exit.
```
