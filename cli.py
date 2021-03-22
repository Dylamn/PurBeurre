#!/usr/bin/python

from typing import Union
from src.cli.components import Auth
from src.cli.components.search import Search
from src.cli.components.menus import MainMenu
from src.cli.components.substitute import Substitute


class Cli:
    """CLI application."""

    __running = False

    _menu: MainMenu

    @property
    def menu(self):
        return self._menu

    __prompt = "{}"

    @property
    def prompt(self):
        """Display the username if an user is authenticated. Else display `guest`
        """
        if self._auth and self._auth.user:
            return self.__prompt.replace('{}', self._auth.user.username)

        return self.__prompt.replace('{}', 'guest')


    # None value means its a guest.
    _auth: Union[None, Auth] = None

    # The message that's to the user when the app starts.
    welcome_message = "Hello! And welcome to the Pur Beurre CLI."

    def __init__(self):
        """Initialize the CLI and its components."""
        self._menu = MainMenu()
        self._search = Search()
        self._auth = Auth()
        self._substitutes = Substitute()

    def handle_action(self, action):
        authenticated = self._auth.authenticated
        if action == 'search':
            self._search.start(self._auth)

        elif authenticated and action == 'registered.products':
            self._substitutes.retrieve_substitutes(self._auth)

        elif not authenticated and action == 'register':
            self._auth.register()

        elif not authenticated and action == 'login':
            self._auth.login()

        elif authenticated and action == 'logout':
            self._auth.logout()

        elif action == 'quit':
            self.__running = False
            # Logout the user before leaving application.
            if self._auth.authenticated:
                self._auth.logout()
                del self._auth

    def run(self):
        self.__running = True

        # Print a welcome message to the user.
        print(self.welcome_message)

        while self.__running:
            # Wait for an user input.
            action = self.menu.show(self.prompt, self._auth.authenticated)

            # Dispatch action.
            self.handle_action(action)

        print('Bye')


def main():
    """Bootstrap the application."""

    # Create the application.
    cli = Cli()

    # Run the app.
    cli.run()


if __name__ == '__main__':
    main()
