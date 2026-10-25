from unittest.mock import patch
from google.genai import errors
from app.llm import generate_answer, ADVANCED_MODEL

with patch(
    "app.llm.select_model",
    return_value=ADVANCED_MODEL
), patch(
    "app.llm.client.models.generate_content"
) as mock_generate:

    mock_generate.side_effect = [
        errors.ServerError(
            503,
            {"error": {"message": "Simulated temporary failure"}}
        ),
        type("FakeResponse", (), {"text": "Fallback worked!"})()
    ]

    answer = generate_answer("Debug this complex algorithm")

    print("Answer:", answer)
    print("Model calls:", mock_generate.call_count)
    print("First model:", mock_generate.call_args_list[0].kwargs["model"])
    print("Fallback model:", mock_generate.call_args_list[1].kwargs["model"])
