import bcrypt
import requests
from typing import Union
from threading import Timer
from getpass import getpass
from src.config import Config
from src.cli.entities.user import User
from src.utils import is_valid_email, input_until_valid, gen_auth_header


class Auth:
    """Class which is the responsible of the authentication.

    Attributes:
        __user (User): Object which represents the user in the database.
        __token (str): The token of the currently logged in user.
        __refresh_token (str): The token used for creating new basic access token.
    """

    __user: Union[User, None]

    __token: Union[str, None]

    __refresh_token: Union[str, None]

    __refresh_thread: Timer

    REFRESH_INTERVAL = 2

    ERROR_PREFIX: str = "(Error)"

    @property
    def user(self):
        return self.__user

    @property
    def token(self):
        """str: Returns the token of the currently logged in user."""
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value
        self.__refresh_thread.cancel()

        if self.__refresh_thread.is_alive():
            self.__refresh_thread.cancel()

        # Create a new thread for the automatic refresh.
        self.__refresh_thread = self.create_refresh_thread(self.REFRESH_INTERVAL)
        self.__refresh_thread.start()

    def __init__(self, token, refresh_token):
        """Log in the user which correspond to the given token.

        Args:
            token: The token which will be used for authenticated requests
            refresh_token: The token used for refreshing the expired access token
        """
        self.__token = token
        self.__user = User(**self.__get_user())
        self.__refresh_token = refresh_token

        # Start automatic refresh token (59 minutes)
        self.__refresh_thread = self.create_refresh_thread(self.REFRESH_INTERVAL)
        self.__refresh_thread.start()

        # Notify the user that's login is completed.
        print(f"You're now logged in! Welcome {self.user.username}.")

    @classmethod
    def register(cls):
        """Display a form and attempt to register him in the database."""
        data = {
            'username': input_until_valid(
                'Enter your username (min 3 characters): ',
                lambda name: len(name.strip()) > 2
            ),
            'email': input_until_valid(
                'Enter your email address: ', is_valid_email
            ).lower()
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
        payload = response.json()

        # An error occurs while inserting the user in the database.
        if response.status_code != 201:
            message = payload.get('message')

            if not message:
                message = "An unexpected error occurred."

            print(message)

            return

        print("Your account has been created.")

        # Retrieve the access and refresh tokens.
        token = payload.get('access_token')
        refresh_token = payload.get('refresh_token')

        return cls(token, refresh_token)

    @classmethod
    def login(cls):
        """Display a form and attempt to log in it with the given credentials"""
        credentials = {
            'email': input_until_valid('Enter your email: ', is_valid_email).lower(),
            'password': getpass().encode('utf-8'),
        }

        response = requests.post(f'{Config.API_URL}/auth/login', credentials)
        payload = response.json()

        if response.status_code != 200:
            return print(
                payload.get(
                    'message',
                    'An unexpected error has occurred.'
                )
            )

        # Retrieve the auth token and set the currently logged in user.
        token = payload.get('access_token')
        refresh_token = payload.get('refresh_token')

        return cls(token, refresh_token)

    def refresh(self):
        """Refresh the access token of the currently authenticated user."""
        if self.user is None or self.token is None:
            self.__refresh_thread.cancel()
            return

        response = requests.post(
            f'{Config.API_URL}/auth/refresh',
            headers=gen_auth_header(self.__refresh_token)
        )

        # Replace the old/expired token by the new one.
        payload = response.json()

        new_token = payload.get('access_token')
        if new_token:
            self.token = new_token
        else:
            print('Your session has expired, please try to log in again.')
            self.logout()

    def logout(self):
        """Logout the currently authenticated user from the application."""
        authorization_header = gen_auth_header(self.token)

        logout_response = requests.post(
            f'{Config.API_URL}/auth/logout',
            headers=authorization_header,
        )

        # Stop the thread process.
        self.__refresh_thread.cancel()

        body = logout_response.json()

        # Notify the user about the logout.
        print(body.get('message'))

        # Token has been blacklisted. Now, flush the current user
        self.__user = None
        self.__token = None

    def create_refresh_thread(self, interval=3600) -> Timer:
        """Create a timed thread for automated token refresh.

        Args:
            interval: The time before the refresh call is triggered.

        Returns:
           threading.Timer
        """
        return Timer(interval, self.refresh)

    def __get_user(self):
        """
        Retrieve the user data by providing an Auth Token.

        Returns:
            dict
        """
        get_user_response = requests.get(
            f'{Config.API_URL}/auth/me',
            headers=gen_auth_header(self.token)
        )

        return get_user_response.json().get('user')