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

    email_regexp = "^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$"

    if re.search(email_regexp, subject):
        return True
    else:
        return False


def input_until_valid(description: str, validator: Callable) -> str:

    user_input = input(description)

    while not validator(user_input):
        user_input = input("(Error) " + description)

    return user_input

def gen_auth_header(token: str) -> dict:
    """
    Generate a dict which contains the Bearer Authorization header
    for authenticated requests.

    :return: dict['str', 'str']
    """
    return {'Authorization': f'Bearer {token}'}

def clear_console() -> None:
    """
    Clean the console output screen.
    """
    from os import system
    from platform import os

    # 'clear' command is used by posix, linux and many other OS
    command = 'cls' if os.name == 'Windows' else 'clear'

    system(command)

def pluck(array: list, key: str, assoc=None):
    """Get values of different dict in a flatten array

        Args:
            array (list): The array to iterate on.
            key (str): The key used for getting values.
            assoc: Append an equal comparaison for each values.
    """
    values = []

    for item in array:
        if key in item:
            if assoc is not None:
                values.append(assoc == item[key])
            else:
                values.append(item[key])

    return values
