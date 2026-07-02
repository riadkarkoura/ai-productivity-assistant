from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
LOGS_DIR = BASE_DIR / "logs"
DB_PATH = BASE_DIR / "database.json"


def ensure_project_directories() -> None:
    """Create folders used by the assistant if they do not exist."""
    for folder in [
        OUTPUTS_DIR,
        OUTPUTS_DIR / "emails",
        OUTPUTS_DIR / "translations",
        OUTPUTS_DIR / "summaries",
        OUTPUTS_DIR / "code",
        OUTPUTS_DIR / "documents",
        LOGS_DIR,
    ]:
        folder.mkdir(parents=True, exist_ok=True)


def get_model() -> str:
    """Read the model name from .env or use a safe default."""
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
