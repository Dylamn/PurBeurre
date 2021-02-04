#!/usr/bin/python

from src.cli.components import Auth
from src.cli.components.menus import MainMenu

class Cli:
    """CLI application."""

    __running = False

    __menu: MainMenu

    @property
    def menu(self):
        return self.__menu

    __prompt = "{}"

    @property
    def prompt(self):
        if self._auth is None:
            return self.__prompt.replace('{}', 'guest')

        return self.__prompt.replace('{}', self._auth.user.username)

    # None value means its a guest.
    _auth: Auth = None

    # The message that's to the user when the app starts.
    welcome_message = "Hello! And welcome to the Pur Beurre CLI."

    def __init__(self):
        self.__menu = MainMenu()

    def handle_action(self, action):
        if action == 'search':
            pass

        elif self._auth and action == 'registered.products':
            pass

        elif not self._auth and action == 'register':
            self._auth = Auth.register()

        elif not self._auth and action == 'login':
            self._auth = Auth.login()

        elif self._auth and action == 'logout':
            del self._auth

        elif action == 'quit':
            self.__running = False

    def run(self):
        self.__running = True

        # Print a welcome message to the user.
        print(self.welcome_message)

        while self.__running:
            # Wait for an user input.
            action = self.menu.show(self.prompt, bool(self._auth))

            # Dispatch action.
            self.handle_action(action)

        # Logout the user before leaving application.
        if bool(self._auth):
            del self._auth

        print('Bye')


def main():
    """Bootstrap the application."""

    # Create the application.
    cli = Cli()

    # Run the app.
    cli.run()


if __name__ == '__main__':
    main()
