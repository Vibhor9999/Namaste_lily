from flask import Flask, request, jsonify
import requests
import datetime
import pyttsx3
import os
from io import BytesIO
from gtts import gTTS

app = Flask(__name__)

# ====== CONFIGURATION ======
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
# ============================

@app.route("/")
def home():
    return "<h2>🌸 Namaste! Lily AI is online and ready.</h2>"

@app.route("/ask", methods=["POST"])
def ask_lily():
    data = request.get_json()
    user_input = data.get("text", "").lower()

    if not user_input:
        return jsonify({"reply": "I didn’t catch that."})

    # Offline logic
    if "time" in user_input:
        reply = f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    elif "date" in user_input:
        reply = f"Today is {datetime.datetime.now().strftime('%B %d, %Y')}."
    elif "your name" in user_input:
        reply = "I am Lily, your personal assistant created by Vibhor Upadhyay."
    elif "creator" in user_input:
        reply = "I was created by Vibhor Upadhyay using Groq AI and Flask technology."
    else:
        # Groq AI response
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": user_input}]
            }
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            if res.status_code == 200:
                reply = res.json()["choices"][0]["message"]["content"].strip()
            else:
                reply = "I'm having trouble connecting to Groq right now."
        except Exception as e:
            print("Error:", e)
            reply = "I couldn’t reach Groq servers."

    # Convert reply to audio
    tts = gTTS(reply)
    audio_path = "reply.mp3"
    tts.save(audio_path)

    return jsonify({"reply": reply, "audio": request.host_url + audio_path})

@app.route("/reply.mp3")
def serve_audio():
    return app.send_static_file("reply.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
