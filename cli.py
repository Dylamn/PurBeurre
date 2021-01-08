from src.cli.auth import Auth


def main(*args):
    """Bootstrap the application."""
    print("Hello! And welcome to the Pur Beurre CLI.")
    running = True

    while running:
        print(
            "What you want to do next?\n",

            "1. Search a product",
            "2. Register your account",
            "3. Leave application",

            sep="\n", end="\n"
        )

        action = input("> ")

        if action == "1":
            pass

        if action == "2":
            Auth.register()

        if action == "3":
            running = False


if __name__ == '__main__':
    main()
