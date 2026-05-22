from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# HOME PAGE
@app.route("/")
def home():

    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()


# CHAT SYSTEM
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data["message"].lower()

    if "hi" in user_message:
        reply = "Yo 👋 I'm Abgrade."

    elif "who are you" in user_message:
        reply = "I'm Abgrade AI. Still evolving."

    elif "bye" in user_message:
        reply = "See you soon ⚡"

    else:
        reply = f"You said: {user_message}"

    return jsonify({
        "reply": reply
    })


# CSS FILE
@app.route("/style.css")
def style():
    with open("style.css", "r", encoding="utf-8") as file:
        return file.read(), 200, {'Content-Type': 'text/css'}


# JS FILE
@app.route("/script.js")
def script():
    with open("script.js", "r", encoding="utf-8") as file:
        return file.read(), 200, {'Content-Type': 'application/javascript'}


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)