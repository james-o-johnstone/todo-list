from flask import Flask

from todo_api import routes
from todo_api.extensions import db, login_manager


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    app.register_blueprint(routes.blueprint)
