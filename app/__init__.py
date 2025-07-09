from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()
api = Api()
csrf = CSRFProtect()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    api.init_app(app)
    login_manager.login_view = 'login'

    from app.routes import main
    app.register_blueprint(main)

    return app