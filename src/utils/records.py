import os
from pathlib import Path
from typing import List


def get_sample_list(recording_path: Path) -> List[str]:
    filenames = os.listdir(recording_path)
    samples = filter_for_game_state_files(filenames)
    return sort_records(samples)


def filter_for_game_state_files(filenames: List[str]) -> List[str]:
    return [record[:-4] for record in filenames if record[-4:] == ".bin"]


def sort_records(filenames: List[str]) -> List[str]:
    return sorted(filenames, key=lambda x: int(x))
