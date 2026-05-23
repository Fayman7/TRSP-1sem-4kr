import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (optional; see .env.example)
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./products.db")
