from pathlib import Path
from os import path


def base_path(relpath: str):
    """Get the path to the base of the project.

    :param relpath relative path to a file, dir...

    """
    base = Path(path.dirname(__file__)).parent

    return base.joinpath(relpath)
