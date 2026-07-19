import os
import re
import time

import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

_model = None
MAX_RETRIES = 3


def get_model():
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-3.1-flash-lite")
    return _model


def _retry_delay(error: ResourceExhausted) -> float:
    match = re.search(r"retry in ([\d.]+)s", str(error), re.IGNORECASE)
    if match:
        return float(match.group(1)) + 1
    return 15


def generate(prompt: str) -> str:
    model = get_model()
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(prompt)
            return response.text
        except ResourceExhausted as e:
            last_error = e
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(_retry_delay(e))
    raise last_error
