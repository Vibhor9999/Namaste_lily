from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# === CONFIG ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set in Render dashboard
GROQ_MODEL = "llama-3.3-70b-versatile"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("text", "")
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": user_input}]
        }
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                          headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            reply = r.json()["choices"][0]["message"]["content"].strip()
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": "Groq connection error."})
    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
