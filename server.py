from src.api import make_app


def main():
    """Bootstrap the application."""
    app = make_app()

    app.app_context().push()

    app.run()


if __name__ == '__main__':
    main()
