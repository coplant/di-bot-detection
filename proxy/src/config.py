from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

DEFAULT_FILE_CHUNK_SIZE = 1024 * 1024 * 5

API_HOST = os.environ.get("API_HOST")
API_PORT = os.environ.get("API_PORT")
STATIC_PATH = os.environ.get("STATIC_PATH")
REDIS_URL = os.environ.get("REDIS_URL")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

EXPIRATION_TIME = os.environ.get("EXPIRATION_TIME")

RATE_LIMITER_COUNT = os.environ.get("RATE_LIMITER_COUNT")
RATE_LIMITER_TIME = os.environ.get("RATE_LIMITER_TIME")
