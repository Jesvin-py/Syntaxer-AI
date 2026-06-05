import json
import os
import importlib

PROVIDER_CONFIG = {
    "gemini": {
        "label":   "Gemini 2.5 Flash",
        "module":  "providers.gemini",
        "env_key": "GEMINI_API_KEY",
        "kwargs":  {},
    },
    "gpt4o-mini": {
        "label":   "GPT-4o Mini",
        "module":  "providers.openrouter",
        "env_key": "OPENROUTER_API_KEY",
        "kwargs":  {"model_key": "gpt4o-mini"},
    },
    "claude": {
        "label":   "Claude Haiku",
        "module":  "providers.openrouter",
        "env_key": "OPENROUTER_API_KEY",
        "kwargs":  {"model_key": "claude"},
    },
    "llama": {
        "label":   "Auto (Free)",
        "module":  "providers.openrouter",
        "env_key": "OPENROUTER_API_KEY",
        "kwargs":  {"model_key": "llama"},
    },
    "mistral": {
        "label":   "Llama 4 Scout (Free)",
        "module":  "providers.openrouter",
        "env_key": "OPENROUTER_API_KEY",
        "kwargs":  {"model_key": "mistral"},
    },
}

FALLBACK = {
    "debug": {
        "has_bug":        False,
        "root_cause":     "Analysis unavailable",
        "explanation":    "The selected provider could not complete the analysis. Try again or switch providers.",
        "fix_steps":      [],
        "corrected_code": ""
    },
    "security": {
        "overall_risk":    "UNKNOWN",
        "vulnerabilities": []
    },
    "learn": {
        "concept":        "N/A",
        "why_it_matters": "Analysis could not complete.",
        "tip":            "Try switching to a different provider or retry in a moment."
    }
}


def friendly_error(label: str, error: Exception) -> str:
    err = str(error).lower()
    if any(x in err for x in ["402", "credits", "afford", "balance"]):          
        return f"{label}: Insufficient credits. Switch to a free provider or top up at openrouter.ai."
    if any(x in err for x in ["401", "invalid_api_key", "authentication", "invalid api key"]):
        return f"{label}: Invalid API key. Check your .env file."
    if any(x in err for x in ["429", "quota", "rate limit", "resource_exhausted", "too many"]):
        return f"{label}: Rate limit hit. Wait a moment or switch providers."
    if any(x in err for x in ["503", "unavailable", "overloaded", "service unavailable"]):
        return f"{label}: Service temporarily unavailable. Try again shortly."
    if any(x in err for x in ["insufficient_quota", "billing", "payment"]):
        return f"{label}: Quota exhausted. Top up credits or switch to a free provider."
    if any(x in err for x in ["context_length", "token"]):
        return f"{label}: Code too long for this model. Try a shorter snippet."
    return f"{label}: {str(error)[:140]}"


def analyze_code(code: str, error_message: str, language: str,
                 mode: str, provider: str = "gemini") -> dict:

    provider = provider.lower().strip()
    config = PROVIDER_CONFIG.get(provider)

    if not config:
        available = ", ".join(PROVIDER_CONFIG.keys())
        return {**FALLBACK, "_error": f"Unknown provider '{provider}'. Available: {available}"}

    env_key = config["env_key"]
    if not os.getenv(env_key):
        return {**FALLBACK,
                "_error": f"{config['label']}: API key not set. Add {env_key} to your .env file."}

    try:
        module = importlib.import_module(config["module"])
        result = module.analyze(
            code, error_message, language, mode, **config["kwargs"]
        )
        result["_provider"] = config["label"]
        return result

    except json.JSONDecodeError:
        return {
            **FALLBACK,
            "_provider": config["label"],
            "_error": f"{config['label']}: Response could not be parsed. Try again."
        }

    except Exception as e:
        return {
            **FALLBACK,
            "_provider": config["label"],
            "_error": friendly_error(config["label"], e)
        }