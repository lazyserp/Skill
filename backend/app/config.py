import os

# Only try to load from .env locally
if os.getenv('RAILWAY_ENVIRONMENT') is None:
    from dotenv import load_dotenv
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dotenv_path = os.path.join(basedir, '.env')
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:12345678@localhost/skillswap')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
