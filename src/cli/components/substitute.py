import requests
from src.config import Config
from src.utils import BColor, gen_auth_header, input_until_valid
from src.cli.entities.product import Product


class Substitute:
    def __init__(self):
        self.url = f'{Config.API_URL}/users/substitutes'

    def retrieve_substitutes(self, auth=None):
        if auth is None:
            return

        rewind = True

        while rewind:
            print(
                BColor.wrap('Your registered substitutes:', 'header'),
                end='\n\n'
            )

            response = requests.get(self.url, headers=gen_auth_header(auth.token))

            payload = response.json()

            if response.status_code != 200:
                return

            rewind = self._show_substitutes(
                payload.get('users_substitutes'),
                auth.token
            )

    def _show_substitutes(self, substitutes, token):
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

        print(
            'If you want to delete a record, enter the corresponding number.',
            'Otherwise, press Q to go back to the main menu.', sep='\n'
        )

        user_input = input_until_valid(
            "Please enter a value: ",
            lambda s: s.lower() == 'q'
                      or s.isdigit() and len(pairs) >= int(s) > 0
        )

        if user_input.lower() == 'q':
            return False

        substitute_to_delete = pairs[int(user_input) - 1]

        response = requests.delete(self.url, data={
            "original_product_id": substitute_to_delete[0].get_key(),
            "substitute_product_id": substitute_to_delete[1].get_key()
        }, headers=gen_auth_header(token))

        if response.status_code == 204:
            print(
                BColor.wrap('The substitute has been deleted.', 'okgreen'),
                end='\n'
            )
        else:
            print(
                BColor.wrap(
                    'An unexpected error occurred, please try again later.',
                    'fail'
                ), end='\n'
            )

            return False

        return True
