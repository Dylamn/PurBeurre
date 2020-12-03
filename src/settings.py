from os import getenv
from dotenv import load_dotenv

# Load and parse the .env file
load_dotenv()

# Application variables
APP_NAME = getenv('APP_NAME', 'PurBeurre')
APP_ENV = getenv('APP_ENV', 'production')
APP_DEBUG = getenv('APP_DEBUG', False)

# Database
DB_URI = getenv('DB_URI')
DB_HOST = getenv('DB_HOST', '127.0.0.1')
DB_PORT = getenv('DB_PORT', '3306')
DB_DATABASE = getenv('DB_DATABASE', 'pur_beurre')
DB_USERNAME = getenv('DB_USERNAME', 'username')
DB_PASSWORD = getenv('DB_PASSWORD', 'password')
