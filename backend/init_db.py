# init_db.py (place in backend/)

from app.routes import db
from app.routes import app

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database re-initialized.")
