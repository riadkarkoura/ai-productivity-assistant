from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .config import OUTPUTS_DIR, ensure_project_directories


def save_output(content: str, filename: str, folder_name: str) -> None:
    ensure_project_directories()
    output_path = OUTPUTS_DIR / folder_name / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    output_path.write_text(content, encoding="utf-8")
    print(f"\nSaved organized copy to: {output_path}")


def show_result(content: str, filename: str) -> None:
    print(content)
    save_output(content, filename, "documents")


def read_multiline_input(title: str) -> str:
    print(f"\n{title}")
    print("Paste your text. Press ENTER on an empty line when you are done.\n")

    lines: list[str] = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    text = "\n".join(lines).strip()
    if not text:
        raise ValueError("No text was entered.")
    return text


def read_file_text() -> str:
    file_path = Path(input("Enter file path:\n> ").strip()).expanduser()
    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"This path is not a file: {file_path}")
    return file_path.read_text(encoding="utf-8")
