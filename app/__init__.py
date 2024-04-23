from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config.config import DevelopmentConfig, ProductionConfig, TestingConfig
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    CORS(app)

    FLASK_ENV = os.environ.get('FLASK_ENV')

    if FLASK_ENV == 'production':
        app.config.from_object(ProductionConfig)
        print("Setting up Production")
    elif FLASK_ENV == 'testing':
        app.config.from_object(TestingConfig)
        print("Setting up Testing")
    else:
        app.config.from_object(DevelopmentConfig)
        print("Setting up Development")

    db.init_app(app)

    with app.app_context():
        from .views import views

        db.create_all()

        return app


application = create_app()
