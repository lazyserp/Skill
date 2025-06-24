from app.routes import db, app
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Parse the DB name and root URL
full_db_url = os.getenv("DATABASE_URL")  # mysql+pymysql://user:pass@host/skill_swap
db_name = full_db_url.rsplit('/', 1)[-1]
root_url = full_db_url.rsplit('/', 1)[0]

# Create database if it doesn't exist
engine = create_engine(root_url)
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    print(f"✅ Database '{db_name}' created or already exists.")

# Create tables in app context
with app.app_context():
    db.create_all()
    print("✅ Tables created in database.")
