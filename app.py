from __future__ import annotations

from .api import ask_ai
from .config import ensure_project_directories
from .database import log_event
from .models import AssistantTask
from .utils import read_file_text, read_multiline_input, save_output, show_result


ensure_project_directories()


def write_email() -> None:
    goal = read_multiline_input("What email do you want to write?")
    system_prompt = """
You are a professional business email writer.
Write clear, polite, and well-structured emails.
Use a natural tone, a clear subject suggestion, greeting, body, and closing.
""".strip()
    result = ask_ai(system_prompt, goal)
    print("\n========== AI Email ==========")
    save_output(result, "email.txt", "emails")
    show_result(result, "email.txt")


def translate_text() -> None:
    target_language = input("Translate to which language? Example: English, German, Arabic\n> ").strip()
    text = read_multiline_input("Enter the text you want to translate:")
    system_prompt = f"You are a professional translator. Translate the user text to {target_language}. Keep the meaning accurate and natural."
    result = ask_ai(system_prompt, text)
    print("\n========== Translation ==========")
    save_output(result, "translation.txt", "translations")
    show_result(result, "translation.txt")


def summarize_text() -> None:
    text = read_multiline_input("Enter the text you want to summarize:")
    system_prompt = """
You are an expert summarizer.
Create a clear summary with:
1. Main idea
2. Important details
3. Action items if any exist
""".strip()
    result = ask_ai(system_prompt, text)
    print("\n========== Summary ==========")
    save_output(result, "summary.txt", "summaries")
    show_result(result, "summary.txt")


def explain_python() -> None:
    code = read_multiline_input("Enter the Python code you want to explain:")
    system_prompt = """
You are a senior Python mentor.
Explain the code step by step in simple language.
Mention what the code does, important functions, and possible improvements.
""".strip()
    result = ask_ai(system_prompt, code)
    print("\n========== Python Explanation ==========")
    save_output(result, "python_explanation.txt", "code")
    show_result(result, "python_explanation.txt")


def improve_code() -> None:
    code = read_multiline_input("Enter the code you want to improve:")
    system_prompt = """
You are a senior software engineer.
Review and improve the code.
Return:
1. Main problems
2. Improved version
3. Explanation of changes
""".strip()
    result = ask_ai(system_prompt, code)
    print("\n========== Code Review ==========")
    save_output(result, "code_review.txt", "code")
    show_result(result, "code_review.txt")


def generate_readme() -> None:
    description = read_multiline_input("Describe your project so I can generate a README:")
    system_prompt = """
You are a technical writer.
Generate a professional GitHub README.md with:
- Project title
- Description
- Features
- Installation
- Environment variables
- Usage
- Project structure
- Future improvements
""".strip()
    result = ask_ai(system_prompt, description)
    print("\n========== README ==========")
    save_output(result, "README_generated.md", "documents")
    show_result(result, "README_generated.md")


def cover_letter() -> None:
    details = read_multiline_input("Paste job details and your experience:")
    system_prompt = """
You are a career assistant.
Write a professional cover letter that is specific, confident, and concise.
Avoid exaggeration and keep it natural.
""".strip()
    result = ask_ai(system_prompt, details)
    print("\n========== Cover Letter ==========")
    save_output(result, "cover_letter.txt", "documents")
    show_result(result, "cover_letter.txt")


def summarize_file() -> None:
    text = read_file_text()
    system_prompt = """
You are an expert document assistant.
Summarize this file clearly and include action items if they exist.
""".strip()
    result = ask_ai(system_prompt, text)
    print("\n========== File Summary ==========")
    save_output(result, "file_summary.txt", "summaries")
    show_result(result, "file_summary.txt")


def show_menu(tasks: list[AssistantTask]) -> None:
    print("\n====== AI Productivity Assistant ======")
    for task in tasks:
        print(f"{task.number}. {task.title}")
    print("0. Exit")


def build_tasks() -> list[AssistantTask]:
    return [
        AssistantTask("1", "Write professional email", write_email),
        AssistantTask("2", "Translate text", translate_text),
        AssistantTask("3", "Summarize text", summarize_text),
        AssistantTask("4", "Explain Python code", explain_python),
        AssistantTask("5", "Review and improve code", improve_code),
        AssistantTask("6", "Generate GitHub README", generate_readme),
        AssistantTask("7", "Write cover letter", cover_letter),
        AssistantTask("8", "Summarize a text file", summarize_file),
    ]


def main() -> None:
    tasks = build_tasks()
    task_map = {task.number: task for task in tasks}

    while True:
        show_menu(tasks)
        choice = input("\nChoose an option:\n> ").strip()

        if choice == "0":
            print("Exiting the program. Goodbye!")
            break

        task = task_map.get(choice)
        if not task:
            print("Invalid choice. Please choose a valid option.")
            continue

        try:
            log_event(f"Started task: {task.title}")
            task.handler()
            log_event(f"Finished task: {task.title}")
        except ValueError as exc:
            print(f"Input error: {exc}")
            log_event(f"Input error in {task.title}: {exc}")
        except RuntimeError as exc:
            print(f"Error: {exc}")
            log_event(f"Runtime error in {task.title}: {exc}")


if __name__ == "__main__":
    main()
