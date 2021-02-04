import bcrypt
import requests
from typing import Union
from getpass import getpass
from src.utils import is_valid_email, input_until_valid, gen_auth_header
from src.config import Config
from src.cli.entities.user import User


class Auth:
    """Class which is the responsible of the authentication.

    Attributes:
        __user (User): Object which represents the user in the database.
        __token (str): The token of the currently logged in user.

    """

    __user: Union[User, None] = None

    __token: Union[str, None] = None

    ERROR_PREFIX: str = "(Error)"

    @property
    def user(self):
        return self.__user

    @property
    def token(self):
        """str: Returns the token of the currently logged in user."""
        return self.__token

    def __init__(self, token):
        """Log in the user which correspond to the given token.

        Args:
            token: JWT Auth Token which will be used to retrieve user data
                from the database.
        """
        self.__token = token
        self.__user = User(**self.__get_user())

        # Notify the user that's login is completed.
        print(f"You're now logged in! Welcome {self.user.username}.")

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
        response = requests.post(f"{Config.API_URL}/auth/register", data)

        # An error occurs while inserting the user in the database.
        if response.status_code != 201:
            print("An unexpected error occurred.")
            return

        print("Your account has been created.")

        # Retrieve the JWT Auth Token.
        token = response.json().get('auth_token')

        return cls(token)

    @classmethod
    def login(cls):
        credentials = {
            'email': input_until_valid('Enter your email: ', is_valid_email),
            'password': getpass().encode('utf-8'),
        }

        response = requests.post(f'{Config.API_URL}/auth/login', credentials)
        body = response.json()

        if response.status_code != 200:
            return print(
                body.get(
                    'message',
                    'An unexpected error has occurred.'
                )
            )

        # Retrieve the auth token and set the currently logged in user.
        token = body.get('auth_token')

        return cls(token)

    def __del__(self):
        authorization_header = gen_auth_header(self.token)

        logout_response = requests.post(
            f'{Config.API_URL}/auth/logout',
            headers=authorization_header,
        )

        body = logout_response.json()

        print(body.get('message'))

        # Token has been blacklisted. Now, flush the current user
        self.__user = None
        self.__token = None

    def __get_user(self):
        """
        Retrieve the user data by providing an Auth Token.

        Returns:
            dict
        """
        get_user_response = requests.get(
            f'{Config.API_URL}/auth/me',
            headers=gen_auth_header(self.__token)
        )

        return get_user_response.json().get('user')
