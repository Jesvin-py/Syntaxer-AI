# Syntaxer AI ⚡

> AI-powered code intelligence — debug smarter, ship securely.

Syntaxer AI lets developers paste their code and instantly receive a structured analysis report covering bugs, security vulnerabilities, and a learning breakdown — all powered by Claude AI.

![Syntaxer AI](static/SLOGO.png)

---

## Features

- 🔍 **Debug Mode** — Finds root causes, explains what went wrong, and returns corrected code
- 🛡️ **Security Mode** — Scans for vulnerabilities with severity ratings (CRITICAL → LOW)
- ⚡ **Shield Scan** — Runs both simultaneously for a full code health report
- 📚 **Learn Panel** — Explains the key concept behind every issue found
- 14 languages supported — Python, JavaScript, TypeScript, Java, C, C++, Go, Rust, PHP, Ruby, Bash, SQL, Kotlin, Swift

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, Prism.js |
| Backend | Python, Flask |
| AI | Anthropic Claude API |
| Deployment | Render (backend) + GitHub Pages (frontend) |

---

## Local Development

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/syntaxer-ai.git
cd syntaxer-ai
```

### 2. Create a virtual environment
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
Create a `.env` file in the root:
```
ANTHROPIC_API_KEY=your_api_key_here
```
Get your key at [console.anthropic.com](https://console.anthropic.com)

### 5. Run the server
```bash
python app.py
```
Open `http://localhost:5000` in your browser.

---

## Deployment

Backend is deployed on [Render](https://render.com).
Frontend is served via Flask — no separate static hosting needed.

---

## Project Structure

```
syntaxer-ai/
├── app.py              ← Flask server
├── analyzer.py         ← Claude API logic
├── prompts.py          ← System prompt and JSON schema
├── requirements.txt    ← Python dependencies
├── .env                ← API key (never committed)
├── .gitignore
├── templates/
│   └── index.html      ← Full frontend
└── static/
    └── SLOGO.png       ← Logo
```

---

## License

MIT License — free to use and modify.
