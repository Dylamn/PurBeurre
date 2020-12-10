from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src.api import make_app, db

app = make_app()

# Import models
from src.api.models.category import Category

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
