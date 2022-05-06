from typing import Tuple


def split_filepath(filepath: str) -> Tuple[str, str]:
    """Splits a filepath into the directory and the filename part.

    Parameters
    ----------
    filepath : str
        The path to the file.

    Returns
    -------
    Tuple[str, str]
        The directory and the filename part.
    """
    splits = filepath.split("/")
    filename = splits[-1]
    path = "/".join(splits[:-1])
    return (path, filename)