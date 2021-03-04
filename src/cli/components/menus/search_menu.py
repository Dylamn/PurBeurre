from selectmenu import SelectMenu


class SearchMenu:
    __options = {
        "categories": {
            "pos": 1,
            "text": "Search by category"
        },
        "products": {
            "pos": 2,
            "text": "Search by product"
        }
    }

    __select_menu: SelectMenu

    def __init__(self):
        self.__select_menu = SelectMenu()

    def show(self):
        choices = [option['text'] for option in self.__options.values()]

        self.__select_menu.add_choices(choices)

        choice = self.__select_menu.select(
            f"Please choose an option (use arrow keys): "
        )

        # Retrieve the key of the user choice.
        for key, sub_dict in self.__options.items():
            if sub_dict.get('text') == choice:
                return key
            pass
