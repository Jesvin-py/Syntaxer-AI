<div align="center">

<img src="static/SLOGO.png" alt="Syntaxer AI Logo" width="120"/>

# Syntaxer AI

### AI-powered code intelligence — debug smarter, ship securely.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-syntaxer--ai.onrender.com-00c8ff?style=for-the-badge)](https://syntaxer-ai.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-AI_Engine-8e44ad?style=for-the-badge&logo=google)](https://deepmind.google/gemini)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46e3b7?style=for-the-badge)](https://render.com)

</div>

---

## What is Syntaxer AI?

Syntaxer AI is a fully deployed, production-grade web application that uses **Google Gemini 2.5 Flash** as an intelligence engine to analyze code and return structured, actionable reports — not a chatbot conversation.

A developer pastes their code, selects an analysis mode, and within seconds receives a clean UI report with severity badges, collapsible vulnerability cards, corrected code with syntax highlighting, and an educational breakdown of what went wrong and why.

It solves two problems that are almost always treated separately:
- 🔍 **Debugging** — *why is my code broken?*
- 🛡️ **Security** — *why is my code dangerous?*

The **Shield Scan** mode runs both simultaneously, making it the most powerful demo of LLM-driven code intelligence in a real product interface.

---

## 🔗 Live Demo

**👉 [https://syntaxer-ai.onrender.com](https://syntaxer-ai.onrender.com)**

Paste any code snippet, select a language and mode, and see the full AI analysis in under 5 seconds.

---

## How It Works — System Architecture

```
User pastes code in browser
        ↓
Frontend (HTML/CSS/JS)
sends POST /analyze with JSON payload
        ↓
Flask backend (app.py)
validates input, calls analyzer
        ↓
analyzer.py builds structured prompt
sends to Gemini 2.5 Flash API
        ↓
Gemini returns strict JSON
(debug + security + learn sections)
        ↓
Flask returns JSON to frontend
        ↓
JavaScript renders cards, badges,
syntax-highlighted corrected code
```

The LLM is used purely as a **structured reasoning engine** — it never speaks directly to the user. Every response is parsed into a defined JSON schema and rendered as a proper product UI. This is intentional: it demonstrates how to integrate LLMs into real applications rather than just wrapping them in a chat interface.

---

## Features

| Feature | Description |
|---|---|
| 🔍 **Debug Mode** | Identifies root cause, explains what went wrong in plain English, returns corrected code |
| 🛡️ **Security Scan** | Detects vulnerabilities (SQLi, XSS, hardcoded secrets, etc.) with CRITICAL/HIGH/MEDIUM/LOW severity ratings |
| ⚡ **Shield Scan** | Runs full debug + security analysis simultaneously in one API call |
| 📚 **Learn Panel** | Explains the key concept behind every issue — turns errors into teachable moments |
| 🎨 **Syntax Highlighting** | Corrected code rendered with Prism.js across 14 languages |
| 📋 **Copy to Clipboard** | One-click copy on all corrected code blocks |
| 📊 **Risk Meter** | Visual overall risk rating with colour-coded severity ring |
| 📱 **Responsive UI** | Fully responsive dark-theme interface, works on mobile and desktop |

**Supported Languages:** Python, JavaScript, TypeScript, Java, C, C++, Go, Rust, PHP, Ruby, Bash/Shell, SQL, Kotlin, Swift

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **AI Engine** | Google Gemini 2.5 Flash | Code analysis, bug detection, vulnerability scanning |
| **Backend** | Python 3.11, Flask 3.1 | REST API, request handling, response routing |
| **Prompt Layer** | Custom JSON schema prompting | Forces structured output — no freeform text |
| **Frontend** | Vanilla HTML, CSS, JavaScript | Zero framework overhead, fast load |
| **Syntax Highlighting** | Prism.js | Code rendering across 14 languages |
| **Deployment** | Render (Web Service) | Production hosting with auto-deploy from GitHub |
| **Environment** | python-dotenv | Secure API key management |

---

## LLM Integration Design

This project demonstrates production-grade LLM integration patterns:

- **Structured output via prompt engineering** — The system prompt enforces a strict JSON schema. The model never returns freeform text, making parsing deterministic and reliable.
- **Fallback handling** — If the model returns malformed JSON (rare with Gemini 2.5 Flash), `analyzer.py` catches the `JSONDecodeError` and returns a safe fallback response instead of crashing.
- **Mode-aware prompting** — The same prompt template adjusts analysis depth based on the selected mode (`debug`, `security`, or `shield`), demonstrating context-driven prompt control.
- **Temperature control** — Set to `0.2` for consistent, reproducible analysis results rather than creative variation.
- **Separation of concerns** — Prompt logic lives in `prompts.py`, API calls in `analyzer.py`, routing in `app.py`, and rendering in `index.html`. Each layer is independently testable.

---

## Project Structure

```
syntaxer-ai/
│
├── app.py                  ← Flask server — routes, validation, response handling
├── analyzer.py             ← Gemini API integration, JSON parsing, fallback logic
├── prompts.py              ← System prompt and strict JSON output schema
├── requirements.txt        ← All Python dependencies (pinned versions)
├── .env                    ← API key (never committed — see .gitignore)
├── .gitignore              ← Excludes .env, venv, __pycache__
│
├── templates/
│   └── index.html          ← Complete frontend (HTML + CSS + JS in one file)
│
└── static/
    └── SLOGO.png           ← Brand logo
```

---

## Local Development

### Prerequisites
- Python 3.8+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey) (free tier available)

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

### 4. Add your API key
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

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
    "error_message": ""
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
| Environment Variable | `GEMINI_API_KEY` = your key |

Auto-deploys on every push to `main` via GitHub integration.

> **Note:** On Render's free tier, the service sleeps after 15 minutes of inactivity. The first request after idle takes ~30 seconds to wake up. This is expected behaviour on the free plan.

---

## What I Learned Building This

- How to engineer prompts that force LLMs to return strict, parseable JSON instead of freeform text
- How to build a clean separation between AI logic, API routing, and frontend rendering
- How to handle LLM response failures gracefully with fallback logic
- How to deploy a Python web service to production with environment-based secret management
- How Gemini 2.5 Flash compares to other models for structured reasoning tasks (fast, consistent, excellent at following JSON schemas)

---

## License

MIT License — free to use, fork, and build on.

---

<div align="center">

Built by **Jesvin** · Powered by **Gemini 2.5 Flash** · Deployed on **Render**

⭐ Star this repo if you found it useful!

</div>
