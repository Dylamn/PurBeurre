import requests
from src.config import Config
from src.cli.components.menus import SearchMenu
from src.cli.entities.product import Product
from src.cli.entities.category import Category
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
        user_input = input_until_valid(
            f"Search {choice}: ",
            lambda text_input: not text_input.isdigit()
        )

        if choice == 'products':
            self.get_resources('product', search=user_input)

        else:  # categories
            self.get_resources('category', search=user_input)

    def get_resources(self, resource_type, search=None, category_tag=None):

        # Set up variables used for a loop.
        page = 1
        loop = True

        # Determines if we're going to pull products or categories...
        resource = 'products' if resource_type == 'product' else 'categories'

        while loop:
            # Clear the console output
            clear_console()

            # parameters for the API call.
            params = {
                "page": page,
                "per_page": 10,
            }

            if search is not None:
                params['q'] = search

            if category_tag is not None:
                params['category_tag'] = category_tag

            response = requests.get(f'{Config.API_URL}/{resource}', params)

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

            if len(body.get(resource)) == 0:
                print(BColor.wrap(
                    f'No {resource} found. Back to the main menu...', 'warning')
                )
                return

            formatted_resources = {
                i: Product(**r) if resource == 'products' else Category(**r)
                for i, r in enumerate(body.get(resource), start=1)
            }

            for index, item in formatted_resources.items():
                print(
                    f'{BColor.wrap(index, "okcyan")}. {item.to_string()}',
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
                                 0 < int(inputstr) <= len(formatted_resources)
            )

            if next_action.isdigit():
                resource_selected = formatted_resources[int(next_action)]

                if resource == 'products':
                    go_back = self._show_product(resource_selected)
                else:
                    # Recursive call...
                    self.get_resources(
                        'product',
                        category_tag=resource_selected.tag
                    )
                    go_back = False

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

    def _show_product(self, product: Product = None):
        """Show all details of the given product."""

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
                print(BColor.wrap(
                    f'No products for the category "{category.get("name")}", '
                    f'skipping...',
                    'warning'
                ))
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
                "Enter your choice (q for cancel, n for the next category): ",
                lambda string: string in ['q', 'n'] or string.isdigit() and
                               len(substitutes) >= int(string) > 0
            )

            if substitute_choice.isdigit() and not self.__auth.authenticated:
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
            elif substitute_choice == 'n':
                continue
            elif substitute_choice.isdigit() and self.__auth.authenticated:
                substitute_selected = substitutes[int(substitute_choice)]

                self.register_substitute(original_product, substitute_selected)

                return

        print(BColor.wrap(
            'No more categories available, back to the menu...', 'warning')
        )

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
