import os
from pathlib import Path
from typing import List


def get_sample_list(recording_path: Path) -> List[Path]:
    filepaths = [x for x in recording_path.glob("**/*.bin")]
    return sort_records(filepaths)


def sort_records(filenames: List[Path]) -> List[Path]:
    return sorted(filenames, key=lambda x: int(x.stem))
