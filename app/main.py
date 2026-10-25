from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.cache import add_to_cache, search_cache
from pydantic import BaseModel

load_dotenv()
app_name = os.getenv("APP_NAME")

app = FastAPI(title=app_name)

class QuestionRequest(BaseModel):
    question: str


class CacheEntryRequest(BaseModel):
    question: str
    answer: str

@app.get("/")
def home():
    return {"message": f"{app_name} is running!"}

@app.get("/config")
def get_config():
    return {"app_name": app_name}



@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/cache")
def check_cache(request: QuestionRequest):
    cached_answer = search_cache(request.question)

    if cached_answer is not None:
        return {
            "cached": True,
            "answer": cached_answer
        }

    return {
        "cached": False,
        "message": "No cached answer found."
    }

@app.post("/cache/add")
def store_cache_entry(request: CacheEntryRequest):
    add_to_cache(request.question, request.answer)

    return {
        "message": "Answer added to cache successfully."
    }