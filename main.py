# source_handbook: week11-hackathon-preparation

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from google import genai
from dotenv import load_dotenv

# Safely load the key from .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Gemini client
# It will automatically look for GEMINI_API_KEY in your environment
try:
    client = genai.Client()
except Exception as e:
    print(f"Failed to initialize Gemini Client. Make sure GEMINI_API_KEY is in your .env file. Error: {e}")

class UserRequest(BaseModel):
    user_input: str
    context: str = ""

@app.post("/api/generate")
async def generate_response(request: UserRequest):
    try:
        # Combine system instructions with user input for Gemini
        prompt = f"System Instruction: You are a helpful assistant. Use this context if provided: {request.context}\n\nUser Question: {request.user_input}"
        
        # Using gemini-2.5-flash as it is fast and efficient for hackathons
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return {"result": response.text}

    except Exception as e:
        print(f"Error during generation: {e}")
        raise HTTPException(status_code=500, detail="AI Generation Failed")