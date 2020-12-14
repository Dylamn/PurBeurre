import unittest
import requests


class ApiTest(unittest.TestCase):
    """Test case used for API endpoints.

    Attributes:
        BASE    The base URL of the API.
    """

    BASE = "http://127.0.0.1:5000/"

    def setUp(self) -> None:
        """Hook method for setting up the test fixture before exercising it."""
        self.request_body = {
            "id": "en:category_test",
            "name": "Category Test",
        }

    def test_category_store_success(self) -> None:
        """Method which verify if a category is stored as expected."""
        response = requests.post(self.BASE + 'categories', self.request_body)

        self.assertEqual(201, response.status_code, response.content)

    def test_category_store_failure(self) -> None:
        """Method which will verify if the validation works as expected."""
        # We remove from the request body the "name" attribute which is required.
        request_body = self.request_body.copy()
        del request_body["name"]

        # Check if the parameter is not present...
        self.assertNotIn('name', request_body)

        response = requests.post(self.BASE + 'categories', request_body)

        self.assertEqual(400, response.status_code, response.content)
