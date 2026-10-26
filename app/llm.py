
import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from app.metrics import increment_metric

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from the .env file")

client = genai.Client(api_key=api_key)

LIGHTWEIGHT_MODEL = "gemini-3.5-flash-lite"
ADVANCED_MODEL = "gemini-3.8-flash"


def select_model(question: str) -> str:
    """
    Select a model based on local question-complexity signals.
    This is a heuristic, not a perfect classifier.
    """
    question_lower = question.lower()

    # Signal 1: Complex tasks and performance problems.
    complex_keywords = [
        "debug", "optimize", "algorithm", "architecture",
        "analyze", "analyse", "compare", "prove",
        "time complexity", "space complexity", "recursion",
        "step by step", "trade-off", "tradeoff",
        "refactor", "design a system",
        "run slowly", "runs slowly", "running slowly",
        "performance issue", "performance problem",
        "not working", "unexpected output",
        "memory leak", "bottleneck", "deadlock",
        "why is my program", "why does my code"
    ]

    for keyword in complex_keywords:
        if keyword in question_lower:
            return ADVANCED_MODEL

    # Signal 2: Code snippets or code-like formatting.
    code_indicators = [
        "```", "def ", "class ", "function ",
        "public static void", "#include", "traceback"
    ]

    for indicator in code_indicators:
        if indicator in question_lower:
            return ADVANCED_MODEL

    # Signal 3: Multiple explicit subquestions.
    if question_lower.count("?") >= 3:
        return ADVANCED_MODEL

    # Default: use the lightweight model.
    return LIGHTWEIGHT_MODEL



def generate_answer(question: str) -> str:
    """
    Generate an answer using the selected model.

    Fall back to the lightweight model only when the
    advanced model encounters a server error (5xx)
    or a rate-limit error (429).
    """
    model = select_model(question)

    if model == ADVANCED_MODEL:
        increment_metric("advanced_model_requests")
    else:
        increment_metric("lightweight_model_requests")

    try:
        response = client.models.generate_content(
            model=model,
            contents=question
        )

    except (errors.ServerError, errors.ClientError) as error:
        # Only advanced-model requests can trigger fallback.
        if model != ADVANCED_MODEL:
            raise

        status_code = getattr(error, "code", None)

        # Retry with the lightweight model only for 5xx or 429.
        should_fallback = (
            isinstance(status_code, int)
            and (
                500 <= status_code < 600
                or status_code == 429
            )
        )

        if not should_fallback:
            raise

        increment_metric("fallback_events")
        increment_metric("lightweight_model_requests")

        response = client.models.generate_content(
            model=LIGHTWEIGHT_MODEL,
            contents=question
        )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return response.text

