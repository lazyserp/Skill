import pymysql
from app import create_app, db  # ✅ Make sure you expose these in __init__.py
import app.models.user  # ✅ Import all other models too (very important)

# MySQL config
MYSQL_USER = 'root'
MYSQL_PASSWORD = '12345678'
MYSQL_HOST = 'localhost'
DATABASE_NAME = 'skillswap'

# Step 1: Create DB if not exists
conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD
)

with conn.cursor() as cursor:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"✅ Database '{DATABASE_NAME}' ensured.")
conn.close()

# Step 2: Create tables using Flask app context
app = create_app()  # 🔁 Your app factory

with app.app_context():
    db.create_all()
    print("✅ Tables created.")
    print("📦 Tables detected:", db.metadata.tables.keys())
