from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

API_HOST = os.environ.get("API_HOST")
API_PORT = os.environ.get("API_PORT")
EXPIRATION_TIME = os.environ.get("EXPIRATION_TIME")
STATIC_PATH = "/static/js/core.js"

DEFAULT_FILE_CHUNK_SIZE = 1024 * 1024 * 5

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
