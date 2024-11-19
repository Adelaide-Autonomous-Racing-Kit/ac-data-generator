from pathlib import Path
from typing import Union


def maybe_create_folders(path: Union[Path, str]):
    """
    If the folders in the path doesn't exist, create them

    :path: Folder path required to exist
    :type path: Path, str
    """
    if isinstance(path, str):
        path = Path(path)
    if path.exists():
        return
    path.mkdir(parents=True)
