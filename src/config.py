from os import getenv
from dotenv import load_dotenv
from src.utils import base_path

# Load and parse the .env file
load_dotenv(base_path('.env'))


class Config:
    ENV = getenv('APP_ENV', 'production')
    FLASK_DEBUG = getenv('APP_DEBUG', False)

    # Database
    DB_CONNECTION = getenv('DB_CONNECTION', 'mysql')
    DB_HOST = getenv('DB_HOST', '127.0.0.1')
    DB_PORT = getenv('DB_PORT', '3306')
    DB_DATABASE = getenv('DB_DATABASE', 'pur_beurre')
    DB_USER = getenv('DB_USER', 'username')
    DB_PASSWORD = getenv('DB_PASSWORD', 'password')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'{DB_CONNECTION}://{DB_USER}:{DB_PASSWORD}' \
                              f'@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

    # Url's
    API_URL = getenv('API_URL', 'http://127.0.0.1:5000')
    OPENFOODFACTS_BASE = getenv(
        'OPENFOODFACTS_BASE', 'https://fr-en.openfoodfacts.org'
    )

    # JWT
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', None)
    JWT_ALGO = getenv('JWT_ALGO', 'HS256')
    JWT_TTL = int(getenv('JWT_TTL', 3600))
    JWT_BLACKLIST_ENABLED=True