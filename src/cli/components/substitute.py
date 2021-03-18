import requests
from src.config import Config
from src.utils import BColor, gen_auth_header
from src.cli.entities.product import Product


class Substitute:

    def retrieve_substitutes(self, auth=None):
        if auth is None:
            return

        response = requests.get(
            f'{Config.API_URL}/users/substitutes',
            headers=gen_auth_header(auth.token)
        )

        payload = response.json()

        if response.status_code != 200:
            return

        self._show_substitutes(payload.get('users_substitutes'))

    def _show_substitutes(self, substitutes):
        pairs = [
            [
                Product(**pair['original_product']),
                Product(**pair['substitute_product'])
            ]
            for i, pair in enumerate(substitutes, start=1)
        ]

        for i, (original, substitute) in enumerate(pairs, start=1):
            print(f"Pair n°{BColor.wrap(i, 'okcyan')}:")
            print("Original product:", original, end='\n\n')
            print("Substitued by:", substitute, '\n\n')


