from flask import Flask
from .config import Config
from .extensions import db, login_manager
from .routes import register_routes

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    register_routes(app, login_manager)

    return app
