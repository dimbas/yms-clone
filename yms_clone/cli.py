import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from . import init_app, db
from .models import Product


app = init_app(os.environ.get('ENV') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Product=Product)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
