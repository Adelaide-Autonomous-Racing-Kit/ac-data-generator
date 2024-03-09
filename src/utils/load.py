from pathlib import Path
from typing import Dict, Union

import cv2
import numpy as np
from src.utils.decode import STATE_DTYPES
import yaml

STRING_KEYS = [
    "tyre_compound",
    "last_time",
    "best_time",
    "split",
    "current_time",
]


def load_yaml(filepath: str) -> Dict:
    """
    Loads a yaml file as a dictionary
    """
    with open(filepath) as file:
        yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_dict


def load_game_state(filepath: str) -> Dict:
    """
    Loads recorded game state np.arrays as a dictionary of observations
        see src.game_capture.state.shared_memory.ac for a list of keys
    """
    with open(filepath, "rb") as file:
        data = file.read()
    return state_bytes_to_dict(data)


def state_bytes_to_dict(data: bytes) -> Dict:
    """
    Converts a game state np.arrays to a dictionary of observations
        see src.game_capture.state.shared_memory for a list of keys
    """
    state_array = np.frombuffer(data, STATE_DTYPES)
    state_dict = {key[0]: value for key, value in zip(STATE_DTYPES, state_array[0])}
    for string_key in STRING_KEYS:
        state_dict[string_key] = (
            state_dict[string_key].tobytes().decode("utf-16").rstrip("\x00")
        )
    return state_dict


def load_image(filepath: Union[Path, str]) -> np.array:
    """
    Loads an image from file.
    :param filepath: Path to image file to be loaded.
    :type filepath: Union[Path,str]
    :return: Image loaded as a numpy array.
    :rtype: np.array
    """
    if isinstance(filepath, Path):
        filepath = str(filepath)
    return cv2.imread(filepath)
