"""
Importing and intializing core modules.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import ConfigVariable

db = SQLAlchemy()
migrate = Migrate()