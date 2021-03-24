#!/usr/bin/python

import threading
from src.utils import BColor
from src.cli.components import Auth
from src.cli.components.search import Search
from src.cli.components.menus import MainMenu
from src.cli.components.substitute import Substitute


class Cli:
    """CLI application."""

    __running = False

    _menu: MainMenu

    __prompt = "{}"

    _auth: Auth

    @property
    def menu(self):
        """Retrieve the `MainMenu` instance."""
        return self._menu

    @property
    def prompt(self):
        """Display the username of the authenticated user else show 'guest'."""
        if self._auth and self._auth.user:
            return self.__prompt.replace('{}', self._auth.user.username)

        return self.__prompt.replace('{}', 'guest')

    def __init__(self):
        """Initialize the CLI and its components."""
        self._menu = MainMenu()
        self._search = Search()
        self._auth = Auth()
        self._substitutes = Substitute()

        # This thread will be started when the CLI start running...
        self.sync_database_thread = threading.Thread(
            target=self.sync_database, daemon=True
        )
        self.api_available = threading.Event()

    def handle_action(self, action):
        """Method which handle the user action.

        A user action is a selection of an option in the select menu (e.g. login)
        """
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
        """The CLI main loop."""
        self.__running = True

        # Start the thread which will sync database with Open Food Facts
        self.sync_database_thread.start()
        self.api_available.wait()

        # Due to an API exception flagged in the thread above...
        if self.__running is False:
            print(BColor.wrap(
                "The API isn't available for the moment or an internal "
                "error occurred.\nPlease try again later.",
                'fail'  # Color of the text (fail means red)
            ))
            return

        # Print a welcome message to the user.
        print("Hello! And welcome to the Pur Beurre CLI.")

        while self.__running:
            # Wait for an user input.
            action = self.menu.show(self.prompt, self._auth.authenticated)

            # Dispatch action.
            self.handle_action(action)

        print('Bye')

    def sync_database(self):
        """Sync database with the Open Food Facts data.

        This method also determines whether the API is available.
        If it is not, the CLI stops working.
        """
        from requests import get, post, ConnectionError
        from src.config import Config

        try:
            ping = get(Config.API_URL)

            if ping.status_code:
                self.api_available.set()  # API is available

            resp = post(f'{Config.API_URL}/imports/products_with_categories')

            if not resp.ok:
                self.__running = False

        except ConnectionError:
            self.__running = False
            self.api_available.set()  # API is not available...


def main():
    """Bootstrap the application."""

    # Create the application.
    cli = Cli()

    # Run the app.
    cli.run()


if __name__ == '__main__':
    main()
