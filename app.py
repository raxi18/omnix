import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Tell Python where to find our HTML (templates) and CSS/JS (static) files
# If you haven't moved them into folders yet, create 'templates' and 'static' folders on GitHub!
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# We use an external provider (like Hugging Face or Google AI Studio) to access Gemma 4 safely
GEMMA_API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-9b-it" 
# Note: You will put your secret API Key in Render's settings, NOT in this code!
API_KEY = os.getenv("GEMMA_API_KEY") 

# This creates the structure for the data coming from your browser
class ChatMessage(BaseModel):
    message: str

# 1. This route loads your cool website interface when you open the link
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 2. This route handles the actual chat logic when you click send
@app.post("/chat")
async def chat_with_omnix(data: ChatMessage):
    user_text = data.message

    # Setup the headers for the AI request
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "inputs": f"<start_of_turn>user\n{user_text}<end_of_turn>\n<start_of_turn>model\n",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }

    try:
        # Send the message to the Gemma model
        response = requests.post(GEMMA_API_URL, json=payload, headers=headers)
        response_json = response.json()
        
        # Extract the AI's text response safely
        if isinstance(response_json, list) and len(response_json) > 0:
            ai_response = response_json.get("generated_text", "Omnix is resting right now. Try again shortly.")
            # Clean up the response formatting if the model returns the prompt back
            ai_response = ai_response.split("<start_of_turn>model\n")[-1].strip()
        else:
            ai_response = "I couldn't reach the stars tonight. Check my API key configuration."

    except Exception as e:
        ai_response = f"Backend Error: Could not connect to Omnix engine."

    return {"response": ai_response}
