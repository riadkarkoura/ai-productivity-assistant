from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from .config import DB_PATH, ensure_project_directories


def load_entries() -> list[dict[str, Any]]:
    ensure_project_directories()
    if not DB_PATH.exists():
        return []
    with DB_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_entries(entries: list[dict[str, Any]]) -> None:
    ensure_project_directories()
    with DB_PATH.open("w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2, ensure_ascii=False)


def log_event(message: str) -> None:
    entries = load_entries()
    entries.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message,
        }
    )
    save_entries(entries)
