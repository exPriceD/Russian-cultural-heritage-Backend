from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .config.config import DevelopmentConfig, ProductionConfig, TestingConfig

import os
from dotenv import load_dotenv
# import redis

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    """app.redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"), port=6379, db=0, encoding='utf-8',
        socket_connect_timeout=int(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT"))
    )"""

    CORS(app, resources={r"/*": {"origins": "https://russian-cultural-heritage.vercel.app/"}})

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
        from .views import api

        db.create_all()

        return app


application = create_app()
