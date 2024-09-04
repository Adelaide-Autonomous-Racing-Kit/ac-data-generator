from pathlib import Path


def maybe_create_folders(path: str):
    """
    If the folders in the path doesn't exist, create them

    :path: Folder path required to exist
    :type path: str
    """
    path = Path(path)
    if path.exists():
        return
    path.mkdir(parents=True)
