from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.api import make_app, db
from src.api.models import *

app = make_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
