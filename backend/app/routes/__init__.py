from .auth import auth_bp
from app.extensions import db

def register_routes(app, login_manager):

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth_bp)
