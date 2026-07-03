from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# AI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Database connection
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["linkedin_generator"]
posts_collection = db["posts"]

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
    generated_text = response.text

    posts_collection.insert_one({
        "topic": request.topic,
        "tone": request.tone,
        "post": generated_text,
        "created_at": datetime.utcnow()
    })

    return {"post": generated_text}

@app.get("/history")
def get_history():
    posts = list(posts_collection.find({}, {"_id": 0}).sort("created_at", -1))
    return {"history": posts}