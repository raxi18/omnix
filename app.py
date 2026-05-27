from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

import sqlite3
import os
import traceback

from datetime import datetime

# =========================================
# LOAD ENV VARIABLES
# =========================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing")

# =========================================
# APP SETUP
# =========================================

app = Flask(__name__)

# =========================================
# OPENROUTER CLIENT
# =========================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    default_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Abgrade AI"
    }
)

# =========================================
# DATABASE SETUP
# =========================================

conn = sqlite3.connect(
    "abgrade.db",
    check_same_thread=False
)

cursor = conn.cursor()

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

        # =====================================
        # LOAD MEMORY
        # =====================================

        memories = get_recent_memories()

        memory_text = ""

        for memory in reversed(memories):

            memory_text += f"""

User: {memory[0]}

Abgrade: {memory[1]}

"""

        # =====================================
        # SYSTEM PROMPT
        # =====================================

        system_prompt = f"""

You are Abgrade AI.

You are futuristic, intelligent,
calm, proactive, natural,
and slightly playful.

You are a personal AI operating system.

Keep responses conversational,
human-like, and concise.

Recent Conversation:
{memory_text}

"""

        # =====================================
        # AI RESPONSE
        # =====================================

        response = client.chat.completions.create(

            model="google/gemma-3-4b-it",

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_message
                }

            ],

            temperature=0.7,
            max_tokens=300
        )

        ai_reply = response.choices[0].message.content or "No response."

        # =====================================
        # SAVE MEMORY
        # =====================================

        save_memory(user_message, ai_reply)

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({
            "reply": str(e)
        }), 500

# =========================================
# CSS FILE
# =========================================

@app.route("/style.css")
def style():

    with open("style.css", "r", encoding="utf-8") as file:

        return file.read(), 200, {
            "Content-Type": "text/css"
        }

# =========================================
# JAVASCRIPT FILE
# =========================================

@app.route("/script.js")
def script():

    with open("script.js", "r", encoding="utf-8") as file:

        return file.read(), 200, {
            "Content-Type": "application/javascript"
        }

# =========================================
# HEALTH CHECK
# =========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "Abgrade online"
    })

# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )