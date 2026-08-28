import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data.db"

APP_TITLE = "PLANETY"
APP_VERSION = "1.0.0"
SECRET_KEY = os.environ.get(
    "APP_SECRET_KEY", "planety-nav-secret-key-change-in-production"
)
CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:7998,http://127.0.0.1:7998",
    ).split(",")
    if origin.strip()
]
