from os import getenv
from dotenv import load_dotenv

# Load and parse the .env file
load_dotenv()

# Database variables
DB_HOST = getenv('DB_HOST', '127.0.0.1')
DB_USER = getenv('DB_USER', 'user')
DB_PASSWORD = getenv('DB_PASSWORD', 'password')
