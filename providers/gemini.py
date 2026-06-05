from google import genai
from google.genai import types
import json
import os
import time
from prompts import SYSTEM_PROMPT


def analyze(code: str, error_message: str, language: str, mode: str) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    user_message = f"""Language: {language}
Mode: {mode}
Error message (if any): {error_message if error_message else 'None provided'}

Code to analyze:
{code}
"""

    last_error = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                )
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
                raw_text = raw_text.strip()
            return json.loads(raw_text)

        except Exception as e:
            last_error = e
            err_str = str(e)
            if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                time.sleep(2 * (attempt + 1))
                continue
            break

    raise last_error