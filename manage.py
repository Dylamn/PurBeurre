from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src.api import make_app, db

app = make_app()

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run(host="127.0.0.1", port=5000):
    app.run(host=host, port=port)


if __name__ == '__main__':
    manager.run()
