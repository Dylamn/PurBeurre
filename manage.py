import flask_migrate
from flask_script import Manager
from src.api import make_app, db
from src.utils import BColor
from sqlalchemy.exc import OperationalError

app = make_app()

app.app_context().push()

manager = Manager(app)

migrate = flask_migrate.Migrate(app, db)

manager.add_command('db', flask_migrate.MigrateCommand)


@manager.command
def run(host="127.0.0.1", port=5000):
    # At each API start, check migrations.
    try:
        check_migrations()
    except OperationalError:
        print(BColor.wrap(
            "API can't etablish a connection to the database. Abort running...",
            "fail"
        ))
        exit(1)

    app.run(host=host, port=port)


def check_migrations():
    """Check if migrations are effective. If not, it try to migrate them."""
    if flask_migrate.current() is None:
        flask_migrate.upgrade()


if __name__ == '__main__':
    manager.run()
