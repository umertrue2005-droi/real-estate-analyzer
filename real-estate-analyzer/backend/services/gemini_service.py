import asyncio
import json
import os
import re
from typing import Any

import google.generativeai as genai

MODEL_NAME = "gemini-2.0-flash"


def _model() -> genai.GenerativeModel | None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


async def generate_text(prompt: str) -> str:
    model = _model()
    if model is None:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    def _generate() -> str:
        response = model.generate_content(prompt)
        result = response.text
        return result

    return await asyncio.to_thread(_generate)


def parse_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if fenced:
        cleaned = fenced.group(1)
    else:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)
