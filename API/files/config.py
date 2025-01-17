import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME_FILES")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
