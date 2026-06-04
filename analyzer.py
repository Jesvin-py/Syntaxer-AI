from google import genai
from google.genai import types
import json
import os
import time
from prompts import SYSTEM_PROMPT


def analyze_code(code: str, error_message: str, language: str, mode: str) -> dict:
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

            try:
                return json.loads(raw_text)
            except json.JSONDecodeError:
                return {
                    "debug": {
                        "has_bug": False,
                        "root_cause": "Could not parse analysis",
                        "explanation": "The analysis returned an unexpected format. Please try again.",
                        "fix_steps": [],
                        "corrected_code": code
                    },
                    "security": {
                        "overall_risk": "UNKNOWN",
                        "vulnerabilities": []
                    },
                    "learn": {
                        "concept": "N/A",
                        "why_it_matters": "Analysis could not complete.",
                        "tip": "Try again with a smaller code snippet."
                    }
                }

        except Exception as e:
            last_error = e
            err_str = str(e)
            if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                wait = 2 * (attempt + 1)
                time.sleep(wait)
                continue
            break

    # All retries exhausted
    return {
        "debug": {
            "has_bug": False,
            "root_cause": "Service temporarily unavailable",
            "explanation": f"The Gemini API is temporarily overloaded. Please try again in a moment. (Details: {str(last_error)[:120]})",
            "fix_steps": ["Wait 10–30 seconds and try again."],
            "corrected_code": code
        },
        "security": {
            "overall_risk": "UNKNOWN",
            "vulnerabilities": []
        },
        "learn": {
            "concept": "API Rate Limiting",
            "why_it_matters": "Production APIs have usage limits and can experience demand spikes. Good apps handle this gracefully with retries.",
            "tip": "Always implement retry logic with exponential backoff when calling external APIs."
        }
    }