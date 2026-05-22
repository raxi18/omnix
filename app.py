from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# CHAT SYSTEM
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data["message"].lower()

    # BASIC AI LOGIC
    if "hi" in user_message:
        reply = "Yo 👋 I'm Abgrade."

    elif "who are you" in user_message:
        reply = "I'm Abgrade AI. Still evolving."

    elif "bye" in user_message:
        reply = "See you soon ⚡"

    elif "how are you" in user_message:
        reply = "Systems stable. Energy levels optimal."

    else:
        reply = f"You said: {user_message}"

    return jsonify({
        "reply": reply
    })


# RUN APP
if __name__ == "__main__":
    app.run(debug=True)