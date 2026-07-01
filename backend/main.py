from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequest(BaseModel):
    topic: str
    tone: str

@app.get("/")
def home():
    return {"message": "Hello, your backend is running!"}

@app.post("/generate")
def generate_post(request: PostRequest):
    prompt = f"Write a LinkedIn post about: {request.topic}. Tone: {request.tone}. Keep it professional and engaging."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"post": response.text}