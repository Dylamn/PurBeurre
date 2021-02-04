from selectmenu import SelectMenu

class MainMenu:
    __options = {
        "search": {
            'pos': 1,
            'auth_required': None,
            'text': "Search a product",
        },
        "registered.products": {
            'pos': 2,
            'auth_required': True,
            'text': "Retrieve my registered products"
        },
        "register": {
            'pos': 3,
            'auth_required': False,
            'text': "Register your account"
        },
        "login": {
            'pos': 4,
            'auth_required': False,
            'text': "Login to your account"
        },
        "logout": {
            'pos': 5,
            'auth_required': True,
            'text': "Logout from your account"
        },
        "quit": {
            'pos': 6,
            'auth_required': None,
            'text': "Quit application"
        },
    }

    __select_menu: SelectMenu

    def __init__(self):
        self.__select_menu = SelectMenu()

    def _prepare_menu(self, authenticated: bool = False):
        menu = {}

        for key, sub_dict in self.__options.items():
            # When no user is authenticated.
            if not authenticated and sub_dict.get('auth_required') is True:
                continue

            # When user is authenticated, we'll not inject
            # register and login options in the selection menu.
            elif authenticated and sub_dict.get('auth_required') is False:
                continue

            menu.setdefault(sub_dict.get('pos'), sub_dict.get('text'))

        return menu

    def show(self, name: str, auth: bool):
        menu = self._prepare_menu(auth)
        self.__select_menu.add_choices(list(menu.values()))

        choice = self.__select_menu.select(f"Hi {name}, what you want to do ?")

        # Retrieve the key of the user choice.
        for key, sub_dict in self.__options.items():
            if sub_dict.get('text') == choice:
                return key
            pass
