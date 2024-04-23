from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config.config import DevelopmentConfig, ProductionConfig, TestingConfig
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

db = SQLAlchemy()


def create_app():
    application = Flask(__name__)

    CORS(application)

    FLASK_ENV = os.environ.get('FLASK_ENV')

    if FLASK_ENV == 'production':
        application.config.from_object(ProductionConfig)
        print("Setting up Production")
    elif FLASK_ENV == 'testing':
        application.config.from_object(TestingConfig)
        print("Setting up Testing")
    else:
        application.config.from_object(DevelopmentConfig)
        print("Setting up Development")

    db.init_app(application)

    with application.app_context():
        from . import views

        db.create_all()

        return application
