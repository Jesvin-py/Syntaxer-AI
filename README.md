<div align="center">

<img src="static/SLOGO.png" alt="Syntaxer AI Logo" width="120"/>

# Syntaxer AI

### AI-powered code intelligence — debug smarter, ship securely.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-syntaxer--ai.onrender.com-00c8ff?style=for-the-badge)](https://syntaxer-ai.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![Providers](https://img.shields.io/badge/AI_Providers-5_Models-8e44ad?style=for-the-badge)](https://openrouter.ai)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46e3b7?style=for-the-badge)](https://render.com)

</div>

---

## What is Syntaxer AI?

Syntaxer AI is a fully deployed, production-grade web application that analyzes code and returns structured, actionable reports — not a chatbot conversation.

A developer pastes their code, selects an analysis mode and an AI provider, and within seconds receives a clean UI report with severity badges, collapsible vulnerability cards, corrected code with syntax highlighting, and an educational breakdown of what went wrong and why.

It solves two problems that are almost always treated separately:
- 🔍 **Debugging** — *why is my code broken?*
- 🛡️ **Security** — *why is my code dangerous?*

The **Shield Scan** mode runs both simultaneously. The system supports **five AI providers** through a unified routing layer — switch between Gemini, GPT-4o Mini, Claude Haiku, Llama 3.3 70B, and a free auto-router from the same interface, with no code changes.

---

## 🔗 Live Demo

**👉 [https://syntaxer-ai.onrender.com](https://syntaxer-ai.onrender.com)**

Paste any code snippet, select a language, provider, and mode — full AI analysis in under 5 seconds.

---

## How It Works — System Architecture

```
User pastes code in browser
        ↓
Frontend (HTML/CSS/JS)
POST /analyze → { code, language, mode, provider }
        ↓
Flask backend (app.py)
validates input, extracts provider key
        ↓
analyzer.py — PROVIDER_CONFIG registry
dispatches to correct provider module
        ↓
        ├── providers/gemini.py      → Gemini 2.5 Flash (direct Google SDK)
        └── providers/openrouter.py  → GPT-4o Mini / Claude Haiku /
                                       Llama 3.3 70B / Auto Free
                                       (OpenRouter OpenAI-compatible API)
        ↓
Provider returns strict JSON
{ debug, security, learn }
        ↓
Flask returns JSON to frontend
        ↓
JavaScript renders severity cards, badges,
syntax-highlighted corrected code, learn panel
```

The LLM is used purely as a **structured reasoning engine** — it never speaks directly to the user. Every response is parsed into a defined JSON schema and rendered as a proper product UI. This is intentional: it demonstrates how to integrate LLMs into real applications rather than just wrapping them in a chat interface.

---

## AI Providers

| Provider | Model | Route | Cost |
|---|---|---|---|
| ⚡ Gemini 2.5 Flash | `gemini-2.5-flash` | Direct Google SDK | Free (Gemini key) |
| 🤖 GPT-4o Mini | `openai/gpt-4o-mini` | OpenRouter | Paid |
| 🔮 Claude Haiku | `anthropic/claude-haiku-4.5` | OpenRouter | Paid |
| 🦙 Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct` | OpenRouter | Paid |
| 🆓 Auto Free | `openrouter/auto` | OpenRouter | Free |

`openrouter/auto` dynamically selects from whatever free models are live — it never 404s when specific free endpoints are retired.

---

## Features

| Feature | Description |
|---|---|
| 🔍 **Debug Mode** | Identifies root cause, explains what went wrong in plain English, returns corrected code |
| 🛡️ **Security Scan** | Detects vulnerabilities (SQLi, XSS, hardcoded secrets, etc.) with CRITICAL/HIGH/MEDIUM/LOW severity ratings |
| ⚡ **Shield Scan** | Runs full debug + security analysis simultaneously in one API call |
| 📚 **Learn Panel** | Explains the key concept behind every issue — turns errors into teachable moments |
| 🤖 **Multi-Provider** | Switch between 5 AI providers with quick-pick pill buttons |
| 🎨 **Syntax Highlighting** | Corrected code rendered with Prism.js across 14 languages |
| 📋 **Copy to Clipboard** | One-click copy on all corrected code blocks |
| 📊 **Risk Meter** | Visual overall risk rating with colour-coded severity ring |
| 📱 **Responsive UI** | Fully responsive dark-theme interface, works on mobile and desktop |

**Supported Languages:** Python, JavaScript, TypeScript, Java, C, C++, Go, Rust, PHP, Ruby, Bash/Shell, SQL, Kotlin, Swift

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **AI Providers** | Gemini 2.5 Flash, GPT-4o Mini, Claude Haiku, Llama 3.3 70B, Auto Free | Code analysis, bug detection, vulnerability scanning |
| **Provider Gateway** | OpenRouter (OpenAI-compatible API) | Unified routing for all non-Gemini providers |
| **Backend** | Python 3.11, Flask 3.1 | REST API, request handling, provider dispatch |
| **Provider Layer** | `providers/gemini.py` + `providers/openrouter.py` | Isolated per-provider logic |
| **Prompt Layer** | Custom JSON schema prompting | Forces structured output — no freeform text |
| **Frontend** | Vanilla HTML, CSS, JavaScript | Zero framework overhead, fast load |
| **Syntax Highlighting** | Prism.js | Code rendering across 14 languages |
| **Deployment** | Render (Web Service) | Production hosting with auto-deploy from GitHub |
| **Environment** | python-dotenv | Secure API key management |

---

## LLM Integration Design

This project demonstrates production-grade LLM integration patterns:

- **Structured output via prompt engineering** — The system prompt enforces a strict JSON schema. The model never returns freeform text, making parsing deterministic and reliable.
- **Provider routing via PROVIDER_CONFIG registry** — `analyzer.py` uses a config-driven registry to dispatch requests to the correct provider module. Adding a new provider requires only one config entry — no changes to routing or frontend logic.
- **OpenRouter as provider gateway** — All non-Gemini providers route through OpenRouter's OpenAI-compatible API. `openrouter/auto` is used as the free-tier slot so it never 404s when specific model endpoints are retired.
- **Friendly error handling** — `friendly_error()` maps raw API exceptions (401, 402, 429, 503) to human-readable messages so users always see actionable feedback instead of stack traces.
- **Fallback handling** — If any provider returns malformed JSON, `analyzer.py` catches the `JSONDecodeError` and returns a safe structured fallback so the frontend never crashes.
- **Mode-aware prompting** — The same prompt template adjusts analysis depth based on the selected mode (`debug`, `security`, or `shield`).
- **Temperature control** — Set to `0.2` for consistent, reproducible analysis results rather than creative variation.
- **Retry with exponential backoff** — Gemini 503/429 errors are retried up to 3 times with 2s, 4s, 6s delays before returning a fallback.
- **Separation of concerns** — Prompt logic in `prompts.py`, provider logic in `providers/`, routing in `app.py`, rendering in `index.html`. Each layer is independently testable.

---

## Project Structure

```
syntaxer-ai/
│
├── app.py                  ← Flask server — routes, validation, provider extraction
├── analyzer.py             ← PROVIDER_CONFIG registry, dispatch, error handling
├── prompts.py              ← System prompt and strict JSON output schema
├── requirements.txt        ← All Python dependencies (pinned versions)
├── .env                    ← API keys (never committed — see .gitignore)
├── .gitignore              ← Excludes .env, venv, __pycache__
│
├── providers/
│   ├── __init__.py         ← Package init
│   ├── gemini.py           ← Gemini 2.5 Flash via direct Google SDK + retry logic
│   └── openrouter.py       ← GPT-4o Mini, Claude Haiku, Llama, Auto Free via OpenRouter
│
├── templates/
│   └── index.html          ← Complete frontend (HTML + CSS + JS in one file)
│
├── static/
│   └── SLOGO.png           ← Brand logo
│
└── docs/                   ← System design document
```

---

## Local Development

### Prerequisites
- Python 3.8+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey) (free)
- An [OpenRouter API key](https://openrouter.ai) (free account, some models need credits)

### 1. Clone the repo
```bash
git clone https://github.com/Jesvin-py/Syntaxer-AI.git
cd Syntaxer-AI
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your free OpenRouter key at [openrouter.ai](https://openrouter.ai). The **Auto Free** provider works with $0 balance.

### 5. Run the server
```bash
python app.py
```
Open `http://localhost:5000` in your browser.

### 6. Test the API directly
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "password = \"admin123\"\nconn = db.execute(\"SELECT * FROM users WHERE id=\" + user_input)",
    "language": "python",
    "mode": "shield",
    "error_message": "",
    "provider": "gemini"
  }'
```

---

## Deployment

The app is deployed as a single Flask service on **Render**, serving both the frontend templates and the `/analyze` API endpoint.

### Render Configuration
| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Environment Variables | `GEMINI_API_KEY` + `OPENROUTER_API_KEY` |

Auto-deploys on every push to `main` via GitHub integration.

> **Note:** On Render's free tier, the service sleeps after 15 minutes of inactivity. The first request after idle takes ~30–50 seconds to wake up. This is expected behaviour on the free plan.

---

## What I Learned Building This

- How to engineer prompts that force LLMs to return strict, parseable JSON instead of freeform text
- How to design a provider routing architecture that isolates each AI provider behind a common interface, making the system extensible without touching core logic
- How to handle provider-specific failure modes (402 credit errors, 404 retired endpoints, 429 rate limits) with a unified friendly error layer
- How to build a clean separation between AI logic, API routing, and frontend rendering
- How to use OpenRouter as a unified gateway for multiple LLM providers through a single OpenAI-compatible API
- How to deploy a Python web service to production with environment-based secret management
- How different models (Gemini, Claude, Llama, Mistral) vary in instruction-following quality for structured JSON output tasks

---

## License

MIT License — free to use, fork, and build on.

---

<div align="center">

Built by **Jesvin** · 5 AI Providers · Deployed on **Render**

⭐ Star this repo if you found it useful!

</div>
