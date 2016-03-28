from flask import Flask
# from app.core.admin import create_admin
from apps.models import db, cache
import apps.views
from flask.ext.login import LoginManager


# install mysqldb for python 3
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


DEFAULT_APP_NAME = 'condorweb'

DEFAULT_MODULES = (
    views.myapp,
)


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config')
    app.config.from_pyfile('../config.py')
    register_database(app)
    register_blueprint(app, DEFAULT_MODULES)
    init_login(app)
    # create_admin(app, db)
    return app


def register_log():
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)


def register_database(app):
    db.init_app(app)
    db.app = app
    cache.init_app(app)


def register_blueprint(app, modules):
    for module in modules:
        app.register_blueprint(module)


# Initialize flask-login
def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'views.loginin'
    # Create user loader function

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models import User
        return User.query.get(int(user_id))





