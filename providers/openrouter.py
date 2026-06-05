from openai import OpenAI
import json
import os
from prompts import SYSTEM_PROMPT

MODELS = {
    "gpt4o-mini":  "openai/gpt-4o-mini",
    "claude":      "anthropic/claude-haiku-4.5",
    "llama":       "meta-llama/llama-3.3-70b-instruct",
    "mistral":     "openrouter/auto",
}


def analyze(code: str, error_message: str, language: str,
            mode: str, model_key: str = "llama") -> dict:

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://syntaxer-ai.onrender.com",
            "X-Title": "Syntaxer AI",
        }
    )

    model = MODELS.get(model_key, MODELS["llama"])

    user_message = f"""Language: {language}
Mode: {mode}
Error message (if any): {error_message if error_message else 'None provided'}

Code to analyze:
{code}
"""

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message}
        ]
    )

    raw_text = response.choices[0].message.content.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    return json.loads(raw_text)