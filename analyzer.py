from google import genai
from google.genai import types
import json
import os
from prompts import SYSTEM_PROMPT


def analyze_code(code: str, error_message: str, language: str, mode: str) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    user_message = f"""Language: {language}
Mode: {mode}
Error message (if any): {error_message if error_message else 'None provided'}

Code to analyze:
{code}
"""

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
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        result = {
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

    return result