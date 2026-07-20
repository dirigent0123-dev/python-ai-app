import os
import re
import time

from google import genai
from google.genai import errors as genai_errors
from dotenv import load_dotenv

load_dotenv()

_client = None
MAX_RETRIES = 3


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")
        _client = genai.Client(api_key=api_key)
    return _client


def _retry_delay(error: Exception) -> float:
    match = re.search(r"retry in ([\d.]+)s", str(error), re.IGNORECASE)
    if match:
        return float(match.group(1)) + 1
    return 15


def generate(prompt: str) -> str:
    client = get_client()
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )
            return response.text
        except genai_errors.ClientError as e:
            if e.code == 429:
                last_error = e
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(_retry_delay(e))
            else:
                raise
    raise last_error
