import requests
import unittest
import string
import random

from src.config import Config


class AuthenticationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.username = 'Jon'
        self.email  = 'jon.snow@example.com'
        self.password = self.__get_random_string(16)

    def test_register_user(self):
        response = requests.post(f'{Config.API_URL}/auth/register', {
            'username': self.username,
            'email': self.email,
            'password': self.password,
        })

        # Check the status which indicate if everything works as expected.
        self.assertEqual(201, response.status_code)

        # Check if the auth_token is present in the response.
        self.assertIn('auth_token', response.json())

    @staticmethod
    def __get_random_string(length):
        return ''.join(
            random.choice(string.ascii_letters) for _ in range(length)
        )
