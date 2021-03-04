import requests
from src.config import Config
from src.cli.components.menus import SearchMenu
from src.utils import input_until_valid


class Search:
    __menu: SearchMenu

    def __init__(self):
        """Bootstrap the Search"""
        self.__menu = SearchMenu()

    def start(self, token=None):
        # User choose if he wants to find many products of a category
        # or products which correlate with its input.
        choice = self.choose()

    def choose(self):
        choice = self.__menu.show()

        return choice

    def handle_choice(self, choice):
        if choice == 'categories':
            self.categories()

        else: # products
            self.products()

    def products(self):
        user_input = input_until_valid(
            "Search a product: ", lambda text_input: not text_input.isdigit()
        )

        requests.post(f'{Config.API_URL}/products/search', {
            "query": ""
        })

        print('product')

    def categories(self):
        user_input = input("Search a category: ")

        print('category')
