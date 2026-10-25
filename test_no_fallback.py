from unittest.mock import patch
from google.genai import errors

from app.llm import generate_answer, ADVANCED_MODEL

with patch(
    "app.llm.select_model",
    return_value=ADVANCED_MODEL
), patch(
    "app.llm.client.models.generate_content"
) as mock_generate:

    mock_generate.side_effect = errors.ClientError(
        400,
        {"error": {"message": "Simulated invalid request"}}
    )

    try:
        generate_answer("Debug this algorithm")
    except errors.ClientError as error:
        print("Caught error code:", error.code)

    print("Total calls:", mock_generate.call_count)

    for call in mock_generate.call_args_list:
        print("Called model:", call.kwargs.get("model"))
