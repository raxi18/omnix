from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()


# =========================
# CHAT SYSTEM
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        user_message = data.get("message", "")

        # AI RESPONSE
        response = ollama.chat(
            model="gemma3:4b",

            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Abgrade AI,
                    a futuristic intelligent assistant.

                    Personality:
                    - calm
                    - smart
                    - confident
                    - natural

                    Keep responses short unless user asks for details.
                    """
                },

                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        ai_reply = response["message"]["content"]

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })


# =========================
# CSS FILE
# =========================
@app.route("/style.css")
def style():

    with open("style.css", "r", encoding="utf-8") as file:
        return file.read(), 200, {
            'Content-Type': 'text/css'
        }


# =========================
# JS FILE
# =========================
@app.route("/script.js")
def script():

    with open("script.js", "r", encoding="utf-8") as file:
        return file.read(), 200, {
            'Content-Type': 'application/javascript'
        }


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)