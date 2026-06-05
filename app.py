from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from analyzer import analyze_code

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data          = request.get_json()
        code          = data.get("code", "").strip()
        error_message = data.get("error_message", "").strip()
        language      = data.get("language", "python")
        mode          = data.get("mode", "shield")
        provider      = data.get("provider", "gemini")

        if not code:
            return jsonify({"error": "No code provided"}), 400
        if len(code) > 5000:
            return jsonify({"error": "Code too long. Please limit to 5000 characters."}), 400

        result = analyze_code(code, error_message, language, mode, provider)

        if "_error" in result:
            return jsonify({"error": result["_error"]}), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)