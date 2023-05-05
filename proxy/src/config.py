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

EXPIRATION_TIME = int(os.environ.get("EXPIRATION_TIME"))

RATE_LIMITER_COUNT = os.environ.get("RATE_LIMITER_COUNT")
RATE_LIMITER_TIME = os.environ.get("RATE_LIMITER_TIME")

CORS_URL = os.environ.get("CORS_URL")

LS_RATIO_MIN = 60
LS_RATIO_MAX = 85
FP_PRIORITY = {
    "browser": 2.0,
    "timezone": 1.7,
    "fonts": 1.5,
    "canvas": 2.5,
    "UA": 1.1,
    "screen": 1.0,
    "webRTC": 3.0,
    "webGL": 1.5,
    "language": 1.3,
}

FP_RATIO = {
    "browser": 0.5,
    "timezone": 0.65,
    "UA": 0.7,
    "webRTC": 0.7,
    "language": 0.85,
}
