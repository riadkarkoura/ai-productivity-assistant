from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from .config import get_model
from .database import log_event


client: Optional[OpenAI] = None


def get_client() -> OpenAI:
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Please add it to the .env file.")
        client = OpenAI(api_key=api_key)
    return client


def ask_ai(system_prompt: str, user_prompt: str) -> str:
    try:
        response = get_client().chat.completions.create(
            model=get_model(),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("OpenAI returned an empty response.")
        log_event(f"AI request completed with model {get_model()}.")
        return content
    except Exception as exc:
        log_event(f"OpenAI request failed: {exc}")
        raise RuntimeError(f"Failed to get a response from OpenAI: {exc}") from exc
