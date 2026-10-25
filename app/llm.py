
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")

client = genai.Client(api_key=api_key)

LIGHTWEIGHT_MODEL = "gemini-3.5-flash-lite"
ADVANCED_MODEL = "gemini-3.8-flash"


def select_model(question: str) -> str:
    """
    Select a model using simple keyword-based routing.
    This is a starting point, not an intelligent classifier.
    """
    complex_keywords = [
        "debug", "optimize", "algorithm", "architecture",
        "complex", "analyze", "compare", "prove",
        "time complexity", "space complexity", "recursion"
    ]

    question_lower = question.lower()

    for keyword in complex_keywords:
        if keyword in question_lower:
            return ADVANCED_MODEL

    return LIGHTWEIGHT_MODEL



def generate_answer(question: str) -> str:
    model = select_model(question)

    try:
        response = client.models.generate_content(
            model=model,
            contents=question
        )

    except Exception:
        if model != ADVANCED_MODEL:
            raise

        # Fall back to the lightweight model if the advanced model fails.
        response = client.models.generate_content(
            model=LIGHTWEIGHT_MODEL,
            contents=question
        )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return response.text

