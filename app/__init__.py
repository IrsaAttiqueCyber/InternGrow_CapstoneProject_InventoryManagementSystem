import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "main.login"


def create_app():

    app = Flask(
    __name__,
    template_folder="../templates"
   )

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Create logs folder
    os.makedirs("logs", exist_ok=True)

    # Application logging
    logging.basicConfig(
        filename="logs/app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Register application routes
    from app.routes import main
    app.register_blueprint(main)

    # Register REST API
    from app.api import api
    app.register_blueprint(api, url_prefix="/api")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app