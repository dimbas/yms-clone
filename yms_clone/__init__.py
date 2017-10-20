from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_bootstrap import Bootstrap

__version__ = '1.0.0'

db = SQLAlchemy()
adm = Admin()
bootstrap = Bootstrap()

app = Flask(__name__)

from .config import configs
from .admin import init_admin
from . import views


def init_app(config_name):
    app.config.from_object(configs[config_name])

    db.init_app(app)

    adm.init_app(app)
    init_admin(adm)

    bootstrap.init_app(app)

    return app
