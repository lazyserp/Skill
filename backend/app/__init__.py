from flask import Flask
from app.extensions import db, login_manager
from app.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
