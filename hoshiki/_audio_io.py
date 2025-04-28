__all__ = [
    "get_default_microphone_name",
    "get_default_speaker_name",
    "get_microphone_index_from_name",
    "list_microphone_names"
]

from typing import cast

import pyaudio  # type: ignore


def get_default_microphone_name() -> str:
    device_info = pyaudio.PyAudio().get_default_input_device_info()

    return cast(str, device_info["name"])


def get_microphone_index_from_name(name: str) -> int:
    driver = pyaudio.PyAudio()
    device_index: int = -1

    for index in range(driver.get_device_count()):
        device_info = driver.get_device_info_by_index(index)

        if device_info["maxInputChannels"] == 0:
            continue
        if device_info['name'] != name:
            continue

        device_index = index
        break

    if device_index == -1:
        raise ValueError(f"invalid microphone '{name}'")

    return device_index


def get_default_speaker_name() -> str:
    device_info = pyaudio.PyAudio().get_default_output_device_info()

    return cast(str, device_info['name'])


def list_microphone_names() -> list[str]:
    names = []

    audio_interface = pyaudio.PyAudio()

    for index in range(audio_interface.get_device_count()):
        device_info = audio_interface.get_device_info_by_index(index)

        if device_info["maxInputChannels"] > 0:
            names.append(device_info["name"])

    return names


def list_speaker_names() -> list[str]:
    names = []

    audio_interface = pyaudio.PyAudio()

    for index in range(audio_interface.get_device_count()):
        device_info = audio_interface.get_device_info_by_index(index)

        if device_info["maxOutputChannels"] > 0:
            names.append(device_info["name"])

    return names
