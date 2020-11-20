from src.settings import DB_HOST, DB_USER, DB_PASSWORD
from src.api import *


def main(*args):
    """Bootstrap the application."""
    print('Hello world!')
    print(Categories().get())


if __name__ == '__main__':
    main()
