import requests
from src.config import Config
from src.cli.components.menus import SearchMenu
from src.cli.entities.product import Product
from src.utils import input_until_valid, clear_console, gen_auth_header, BColor
from time import sleep


class Search:
    __menu: SearchMenu

    def __init__(self):
        """Bootstrap the Search"""
        self.__menu = SearchMenu()
        self.__auth = None

    def start(self, auth=None):
        self.__auth = auth
        # User choose if he wants to find many products of a category
        # or products which correlate with its input.
        choice = self.choose()

        self.handle_choice(choice)

        self.__auth = None

    def choose(self):
        choice = self.__menu.show()

        return choice

    def handle_choice(self, choice):
        if choice == 'categories':
            self.categories()

        else:  # products
            self.products()

    def products(self):
        user_input = input_until_valid(
            "Search a product: ", lambda text_input: not text_input.isdigit()
        )

        # Set up variables used for a loop.
        page = 1
        loop = True

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

                go_back = self.show_product(product_selected)

                if go_back:  # If true return to the product listing...
                    continue
                else:
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

    def categories(self):
        user_input = input_until_valid(
            "Search a category: ", lambda text_input: not text_input.isdigit()
        )

        print('category')

    def show_product(self, product: Product = None):
        # Clear console output
        clear_console()

        print(product.get_details())

        action = input_until_valid(
            'Do you want to find substitutes for it? (Y/n)\n',
            lambda s: s.lower() in ['y', 'n']
        ).lower()

        if action == 'y':
            # Search for substitutes...
            self.find_substitutes(product)

            return False
        else:
            return True

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

            print(
                f'Choose a substitute for "{original_product.name}" '
                f'in the list above (category "{category["name"]}")',
                end='\n'
            )

            substitute_choice = input_until_valid(
                "Enter your choice (q for cancel): ",
                lambda string: string == 'q' or string.isdigit() and
                               len(substitutes) >= int(string) > 0
            )

            if substitute_choice != 'q' and self.__auth.authenticated is False:
                print(
                    "You are not logged in, please create an account or log in"
                    "to be able to register this substitute.", end='\n\n'
                )
                choice = input_until_valid(
                    'Register: R | Login: L | Abort: Q \n',
                    lambda s: s.lower() in ['r', 'l', 'q']
                ).lower()

                # Choices for authentication...
                if choice == 'q':
                    return
                else:  # The user will register / login...
                    while self.__auth.authenticated is False:
                        if choice == 'r':
                            self.__auth.register()
                        else:
                            self.__auth.login()

            # Choices for substitute selection...
            if substitute_choice == 'q':
                return
            elif substitute_choice.isdigit() and self.__auth.authenticated:
                substitute_selected = substitutes[int(substitute_choice)]

                self.register_substitute(original_product, substitute_selected)

                return

    def register_substitute(self, original: Product, substitute: Product):
        """Register"""
        response = requests.post(f'{Config.API_URL}/users/substitutes', {
            'original_product_id': original.get_key(),
            'substitute_id': substitute.get_key()
        }, headers=gen_auth_header(self.__auth.token))

        payload = response.json()

        if "message" in payload:
            if response.status_code == 201:
                print(BColor.wrap(payload.get('message'), 'okgreen'))
            else:
                print(BColor.wrap(payload.get('message'), 'fail'))
        else:
            print(
                BColor.wrap(
                    "An unexpected error occurred. Please try again later.",
                    'fail'
                )
            )

        return
