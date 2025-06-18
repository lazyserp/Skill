import os
from dotenv import load_dotenv

# ✅ Load .env from absolute path
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))
load_dotenv(dotenv_path)  # 🔥 THIS ensures .env is loaded properly

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
