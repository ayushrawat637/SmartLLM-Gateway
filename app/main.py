from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.cache import add_to_cache, search_cache
from pydantic import BaseModel, Field, field_validator
from app.llm import generate_answer
from app.metrics import increment_metric, get_metrics

load_dotenv()
app_name = os.getenv("APP_NAME")

app = FastAPI(title=app_name)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Question cannot be empty or whitespace only"
            )
        return value


class CacheEntryRequest(BaseModel):
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)

    @field_validator("question")
    @classmethod
    def cache_question_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Question cannot be empty or whitespace only"
            )
        return value

    @field_validator("answer")
    @classmethod
    def answer_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Answer cannot be empty or whitespace only"
            )
        return value


@app.get("/")
def home():
    return {"message": f"{app_name} is running!"}


@app.get("/config")
def get_config():
    return {"app_name": app_name}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics_endpoint():
    return get_metrics()


@app.post("/cache")
def check_cache(request: QuestionRequest):
    cached_answer = search_cache(request.question)

    if cached_answer is not None:
        increment_metric("cache_hits")

        return {
            "cached": True,
            "answer": cached_answer
        }

    increment_metric("cache_misses")

    answer = generate_answer(request.question)

    add_to_cache(request.question, answer)

    return {
        "cached": False,
        "answer": answer
    }




@app.post("/cache/add")
def store_cache_entry(request: CacheEntryRequest):
    add_to_cache(request.question, request.answer)

    return {
        "message": "Answer added to cache successfully."
    }