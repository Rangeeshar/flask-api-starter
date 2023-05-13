"""
Factory pattern for creating flask API object.
"""
import os
import logging.config
from os import environ
from flask_api import FlaskAPI
from dotenv import load_dotenv
from flask_cors import CORS
from importlib import import_module
from .config import config as app_config
from app import db

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app(app_name=PKG_NAME, **kwargs):
    # Loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    # Logging
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = FlaskAPI(app_name)
    # Load Configs
    app.config.from_object(os.environ['APP_SETTINGS'])
    # Modify CORS according to config if required
    CORS(app, resources={r"/*": {"origins": "*"}})
    # Extension registration
    register_extensions(app)
    # Blueprint Registration
    register_blueprints(app)
    return app

def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'