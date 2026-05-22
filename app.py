from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

import sqlite3
import os

from datetime import datetime

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================================
# APP SETUP
# =========================================

app = Flask(__name__)

# =========================================
# OPENROUTER CLIENT
# =========================================

client = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=API_KEY
)

# =========================================
# DATABASE
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
# HOME
# =========================================

@app.route("/")
def home():

    with open("index.html", "r", encoding="utf-8") as file:

        return file.read()

# =========================================
# CHAT
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message", "")

        # =====================================
        # MEMORY
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

You are:
- futuristic
- intelligent
- calm
- proactive
- natural
- slightly playful

You are a personal AI operating system.

You help with:
- productivity
- schedules
- tasks
- reminders
- life management

Keep responses realistic and conversational.

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

            temperature=0.7
        )

        ai_reply = response.choices[0].message.content

        # =====================================
        # SAVE MEMORY
        # =====================================

        save_memory(user_message, ai_reply)

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

# =========================================
# CSS
# =========================================

@app.route("/style.css")
def style():

    with open("style.css", "r", encoding="utf-8") as file:

        return file.read(), 200, {
            'Content-Type': 'text/css'
        }

# =========================================
# JS
# =========================================

@app.route("/script.js")
def script():

    with open("script.js", "r", encoding="utf-8") as file:

        return file.read(), 200, {
            'Content-Type': 'application/javascript'
        }

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(debug=True)