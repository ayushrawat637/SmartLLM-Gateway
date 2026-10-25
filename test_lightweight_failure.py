from unittest.mock import patch
from google.genai import errors

from app.llm import generate_answer, LIGHTWEIGHT_MODEL


with patch(
    "app.llm.select_model",
    return_value=LIGHTWEIGHT_MODEL
), patch(
    "app.llm.client.models.generate_content"
) as mock_generate:

    mock_generate.side_effect = errors.ServerError(
        503,
        {"error": {"message": "Simulated failure"}}
    )

    try:
        generate_answer("What is Python?")
    except errors.ServerError:
        print("PASS: Lightweight error propagated; no fallback attempted.")

    print("Model calls:", mock_generate.call_count)
