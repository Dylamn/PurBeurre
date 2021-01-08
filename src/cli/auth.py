import requests
from getpass import getpass
import bcrypt
from src.utils import is_valid_email, input_field


class Auth:
    """Class which is the responsible of the users registration/authentication."""

    @staticmethod
    def register():
        """Method used in order to register a new user."""
        data = {
            'username': input_field(
                'Enter your username (min 3 characters): ', lambda x: len(x) > 2
            ),
            'email': input_field('Enter your email address: ', is_valid_email)
        }

        password = getpass("Type your password (min 8 characters): ")

        while len(password) < 8:
            password = getpass("Type your password (min 8 characters): ")

        password_confirmed = getpass('Retype your password: ')

        while password != password_confirmed:
            password_confirmed = getpass('Retype your password: ')

        data['password'] = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # Register the user to the API.
        response = requests.post("http://127.0.0.1:5000/users", data)

        if response.status_code == 201:
            print("Your account has been created.")
