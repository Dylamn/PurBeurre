import requests
from src.config import Config
from src.cli.components.menus import SearchMenu
from src.cli.entities.product import Product
from src.utils import input_until_valid, clear_console, BColor
from time import sleep


class Search:
    __menu: SearchMenu

    def __init__(self):
        """Bootstrap the Search"""
        self.__menu = SearchMenu()

    def start(self, auth=None):
        # User choose if he wants to find many products of a category
        # or products which correlate with its input.
        choice = self.choose()

        self.handle_choice(choice)

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

        # Set up variables used for a loop.
        page = 1
        loop = True
        product_selected = None

        while loop:
            # Clear the console output
            clear_console()

            response = requests.get(f'{Config.API_URL}/products', {
                "q": user_input,
                "page": page
            })

            if response.status_code != 200:
                print(
                    BColor.wrap(
                        "An error occurred with the API. Please try again later.",
                        'warning'
                    )
                )
                return

            body = response.json()
            last_page = body.get('meta')['last_page']

            if len(body.get('products')) == 0:
                print('No product found. Back to the main menu...')
                return

            formatted_products = {
                i: Product(**p)
                for i, p in enumerate(body.get('products'), start=1)
            }

            for index, product in formatted_products.items():
                print(
                    f'{BColor.wrap(index, "okcyan")}. {product.to_string()}',
                    end='\n\n'
                )

            print(
                'Page %s / %s' % (body.get('meta')['current_page'], last_page),
                end='\n'
            )
            print('Previous: p | Next: n | Quit: q', end='\n\n')

            # Next action of the user.
            # The user can select a product or request the next page.
            next_action = input_until_valid(
                'Select a product or switch page: ',
                lambda inputstr: inputstr in ['p', 'n', 'q'] or
                                 inputstr.isdigit() and
                                 0 < int(inputstr) <= len(formatted_products)
            )

            if next_action.isdigit():
                product_selected = formatted_products[int(next_action)]

                # Leave the loop
                loop = False
            elif next_action in ['p', 'n']:  # Change the page
                # Increment the page based on the input.
                page = page + 1 if next_action == 'n' else page - 1

                if page > body.get('meta')['last_page']:
                    page = 1
                elif page < 1:
                    page = body.get('meta')['last_page']
            else:  # Quit the menu (next_action value is 'q')
                return
        # End while

        self.show_product(product_selected)

    def categories(self):
        user_input = input_until_valid(
            "Search a category: ", lambda text_input: not text_input.isdigit()
        )

        print('category')

    def show_product(self, product: Product = None):

        # TODO: make a overview of the product
        # print(product.get_details())
        # A product is selected. Search for substitutes
        self.find_substitutes(product)

    def find_substitutes(self, original_product: Product = None):
        """Find substitute(s) for the given product"""
        if original_product is None:
            return

        reversed_categories = reversed(original_product.categories)

        for category in reversed_categories:
            response = requests.get(f'{Config.API_URL}/products', {
                "substituate": original_product.get_key(),
                "category_tag": category.get('tag')
            })

            if response.status_code != 200:
                print(
                    BColor.wrap(
                        'An unexpected error occurred. Please try again later.',
                        'warning'
                    )
                )
                return

            # Retrieve the JSON payload...
            payload = response.json()

            substitutes = {
                i: Product(**s) for i, s in enumerate(
                    payload.get('substitutes'), start=1
                )
            }

            # Clear the console output
            clear_console()

            print(
                f'Choose a substitute for "{original_product.name}" '
                f'in the list below (category "{category["name"]}"):',
                end='\n\n'
            )

            if len(substitutes) == 0:  # Skip to the next category...
                print(
                    f'No products for the category "{category.get("name")}",',
                    f'skipping...'
                )
                # Wait 1 second to let the time for the user to see the message.
                sleep(1)
                continue

            for pos, substitute in substitutes.items():
                print(
                    f'{BColor.wrap(pos, "okcyan")}. {substitute}',
                    end='\n\n'
                )

            substitute_choice = int(input_until_valid(
                "Enter your choice (product number): ",
                lambda string: string.isdigit() and
                            len(substitutes) >= int(string) > 0 or
                            string == 'q'
            ))

            if substitute_choice == 'q':
                return
            else:
                break
