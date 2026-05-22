from flask import Flask, request, jsonify
import google.generativeai as genai
import sqlite3
from datetime import datetime

# =========================================
# APP SETUP
# =========================================

app = Flask(__name__)

# =========================================
# GEMINI SETUP
# =========================================

API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================================
# DATABASE SETUP
# =========================================

conn = sqlite3.connect("abgrade.db", check_same_thread=False)

cursor = conn.cursor()

# MEMORY TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    ai_reply TEXT,
    timestamp TEXT
)
""")

conn.commit()

# =========================================
# MEMORY FUNCTIONS
# =========================================

def save_memory(user_message, ai_reply):

    cursor.execute("""
    INSERT INTO memories (
        user_message,
        ai_reply,
        timestamp
    )
    VALUES (?, ?, ?)
    """, (

        user_message,
        ai_reply,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()


def get_recent_memories(limit=6):

    cursor.execute("""
    SELECT user_message, ai_reply
    FROM memories
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    return cursor.fetchall()

# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

# =========================================
# CHAT SYSTEM
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "")

        # GET MEMORY
        memories = get_recent_memories()

        memory_text = ""

        for memory in reversed(memories):

            memory_text += f"""
User: {memory[0]}
Abgrade: {memory[1]}
"""

        # SYSTEM PROMPT
        prompt = f"""

You are Abgrade AI.

You are:
- futuristic
- intelligent
- calm
- proactive
- human-like
- slightly playful

You are not a basic chatbot.

You are a personal AI operating system
that helps manage the user's life,
tasks, schedule, productivity,
and notifications.

Keep responses natural and realistic.

Recent Conversation:
{memory_text}

Current User Message:
{user_message}

"""

        # GEMINI RESPONSE
        response = model.generate_content(prompt)

        ai_reply = response.text

        # SAVE MEMORY
        save_memory(user_message, ai_reply)

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

# =========================================
# CSS FILE
# =========================================

@app.route("/style.css")
def style():

    with open("style.css", "r", encoding="utf-8") as file:

        return file.read(), 200, {
            'Content-Type': 'text/css'
        }

# =========================================
# JAVASCRIPT FILE
# =========================================

@app.route("/script.js")
def script():

    with open("script.js", "r", encoding="utf-8") as file:

        return file.read(), 200, {
            'Content-Type': 'application/javascript'
        }

# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    app.run(debug=True)