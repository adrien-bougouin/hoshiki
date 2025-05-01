import logging
import sys
import time

import click

from hoshiki import Config, interpreters
from hoshiki._audio_io import \
    get_default_microphone_name, get_default_speaker_name, \
    list_microphone_names, list_speaker_names


LOGGING_FORMAT = "[%(asctime)s][%(name)s] %(levelname)s -- %(message)s"


# TODO: --whisper-context INITIAL_PROMPT


@click.command(help="Consecutive Any-to-English interpreter.")
@click.argument("source-language", required=False, type=click.STRING)
@click.option(
    "--interpreter",
    type=click.Choice(["whisper-translate"]),
    default="whisper-translate", show_default=True,
    help="Name of the interpreter to use."
)
@click.option(
    "--speech-synthesizer",
    type=click.Choice(["stdout", "darwin"]),
    default="stdout", show_default=True,
    help="Name of the speech synthesizer to use."
)
@click.option(
    "--only", metavar="LANGUAGE",
    type=click.STRING, multiple=True,
    help="Selects which source language to transcribe. Only works when"
         " SOURCE_LANGUAGE is not provided (and language is automatically"
         " detected)."
)
@click.option(
    "--input-device", metavar="MICROPHONE_NAME",
    type=click.STRING,
    default=get_default_microphone_name(), show_default=False,
    help="Name of the microphone device to record from (e.g. \"MacBook Pro"
         " Microphone\"). List available devices with '--input-device ?'."
)
@click.option(
    "--output-device", metavar="SPEAKER_NAME",
    type=click.STRING,
    default=get_default_speaker_name(), show_default=False,
    help="Name of the speaker device to speak into (e.g. \"MacBook Pro"
         " Speakers\"). List available devices with '--output-device ?'."
)
@click.option(
    "--whisper-model", metavar="MODEL_NAME",
    type=click.STRING,
    default="base", show_default=True,
    help="Name of the whisper model to use. Option available for the"
         " whisper-translate interpreter, the openai-whisper backend, the"
         " faster-whisper backend, and the whispercpp backend."
)
@click.option(
    "--whisper-backend",
    type=click.Choice(["openai-whisper", "faster-whisper", "whispercpp"]),
    default="openai-whisper", show_default=True,
    help="Whisper backend to use. Option available for the whisper-translate"
         " interpreter."
)
@click.option(
    "--openai-whisper-fp16", is_flag=True,
    help="Use half-precision floating point numbers (instead of"
         " full-precision), for faster and more memory efficient"
         " speech-to-text processing with the openai-whisper backend with"
         " GPU."
)
@click.option(
    "--faster-whisper-compute-type",
    type=click.Choice([
        "int8", "int8_float32", "int8_float16", "int8_bfloat16",
        "int16", "float16", "bfloat16",
        "float32"
    ]),
    default="float32", show_default=True,
    help="Numerical precision, for better managing the speed and the memory"
         " usage of the speech-to-text processing with the faster-whisper"
         " backend."
)
@click.option(
    "-v", "--verbose", is_flag=True,
    help="Print operation details."
)
@click.option(
    "-d", "--debug", is_flag=True,
    help="Print internal operation details."
)
def run(debug: bool = False, verbose: bool = False, **config: Config) -> None:
    if debug:
        logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

    logging.getLogger("hoshiki").debug("Configuration: %s", config)

    if list_devices(config):
        sys.exit(0)

    interprete(config)


def interprete(config: Config) -> None:
    interpreter = interpreters.get(config)

    interpreter.start()

    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        interpreter.stop(1.0)


def list_devices(config: Config) -> bool:
    list_input_devices = config.get("input_device") == "?"
    list_output_devices = config.get("output_device") == "?"

    if list_input_devices:
        print("Input devices:")
        for name in list_microphone_names():
            print(f"  - {name}")

    if list_output_devices:
        print("Output devices:")
        for name in list_speaker_names():
            print(f"  - {name}")

    return list_input_devices or list_output_devices


if __name__ == "__main__":
    run()
