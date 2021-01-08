from pathlib import Path
from os import path
from typing import Callable

def base_path(relpath: str):
    """Get the path to the base of the project.

    :param relpath relative path to a file, dir...
    """
    base = Path(path.dirname(__file__)).parent

    return base.joinpath(relpath)


def is_valid_email(subject):
    """Verify if the given subject is a valid email pattern.

    :param subject The string which will be analysed.
    """
    import re

    email_regexp = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    if re.search(email_regexp, subject):
        return True
    else:
        return False


def input_field(description: str, validator: Callable, *args):
    user_input = input(description)

    while not validator(user_input):
        user_input = input(description)

    return user_input

def is_valid_b_string(string: str):
    return string.isascii()
