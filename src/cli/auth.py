import requests
import bcrypt
from getpass import getpass
from src.utils import is_valid_email, input_until_valid
from src.config import Config
from src.cli.entities.user import User

class Auth:
    """Class which is the responsible of the users registration/authentication."""

    ERROR_PREFIX = "(Error)"

    def __init__(self, user):

        if isinstance(user, User):
            self._user = user

        raise Exception()

    @classmethod
    def register(cls):
        """Method used in order to register a new user."""
        data = {
            'username': input_until_valid(
                'Enter your username (min 3 characters): ',
                lambda x: len(x.strip()) > 2
            ),
            'email': input_until_valid(
                'Enter your email address: ', is_valid_email
            )
        }

        password_is_valid = False
        password = None
        error_prefix_password = ""

        while not password_is_valid:
            if password is not None:
                error_prefix_password = cls.ERROR_PREFIX

            password = getpass(
                "{} Type your password (min 8 characters): ".format(
                    error_prefix_password
                )
            )

            if len(password) >= 8:
                password_is_valid = True

        password_is_confirmed = False
        while not password_is_confirmed:
            password_confirmed = getpass('Retype your password: ')

            if password == password_confirmed:
                password_is_confirmed = True

        data['password'] = bcrypt.hashpw(
            password.encode('utf8'),
            bcrypt.gensalt()
        )

        # Register the user to the API.
        response = requests.post(Config.API_URL + '/users', data)

        if response.status_code == 201:
            print("Your account has been created.")

    @classmethod
    def login(cls):
        credentials = {
            'email': input_until_valid('Enter your email: ', is_valid_email),
            'password': getpass().encode('utf-8'),
        }

        response = requests.post(Config.API_URL + '/auth/login', credentials)
        body = response.json()

        if response.status_code != 200:
            return print(body.message)

        print("You're now logged in!")
