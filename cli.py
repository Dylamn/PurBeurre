from src.cli.auth import Auth


def main():
    """Bootstrap the application."""
    print("Hello! And welcome to the Pur Beurre CLI.")
    running = True

    while running:
        print(
            "What you want to do next?\n",

            "1. Search a product",
            "2. Register your account",
            "3. Login to your account",
            "4. Leave application",

            sep="\n", end="\n"
        )

        action = input("guest: ")

        if action == '1':
            pass

        elif action == '2':
            auth = Auth.register()

        elif action == '3':
            auth = Auth.login()

        elif action in ['4', 'exit']:
            running = False


if __name__ == '__main__':
    main()
