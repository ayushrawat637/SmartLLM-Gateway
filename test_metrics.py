
from unittest.mock import patch, Mock

from app import llm
from app.metrics import metrics


# Reset all counters for a clean test.
for name in metrics:
    metrics[name] = 0


# Test 1: Lightweight model request.
fake_response = Mock()
fake_response.text = "Test answer"

with patch.object(
    llm,
    "select_model",
    return_value=llm.LIGHTWEIGHT_MODEL
), patch.object(
    llm.client.models,
    "generate_content",
    return_value=fake_response
) as mock_generate:

    answer = llm.generate_answer("Simple question")

    assert answer == "Test answer"
    assert metrics["lightweight_model_requests"] == 1
    assert metrics["advanced_model_requests"] == 0
    assert mock_generate.call_count == 1

print("PASS: Lightweight model metrics")


# Test 2: Advanced model fails with 503, then fallback succeeds.
for name in metrics:
    metrics[name] = 0

with patch.object(
    llm,
    "select_model",
    return_value=llm.ADVANCED_MODEL
), patch.object(
    llm.client.models,
    "generate_content",
    side_effect=[
        llm.errors.ServerError(
            503,
            {"error": {"code": 503, "message": "Mock error"}}
        ),
        fake_response
    ]
) as mock_generate:

    answer = llm.generate_answer("Complex question")

    assert answer == "Test answer"
    assert metrics["advanced_model_requests"] == 1
    assert metrics["lightweight_model_requests"] == 1
    assert metrics["fallback_events"] == 1
    assert mock_generate.call_count == 2

print("PASS: Advanced model and fallback metrics")

# Test 3: Both the advanced request and fallback fail.
for name in metrics:
    metrics[name] = 0

with patch.object(
    llm,
    "select_model",
    return_value=llm.ADVANCED_MODEL
), patch.object(
    llm.client.models,
    "generate_content",
    side_effect=[
        llm.errors.ServerError(
            503,
            {"error": {"code": 503, "message": "Advanced unavailable"}}
        ),
        llm.errors.ServerError(
            503,
            {"error": {"code": 503, "message": "Fallback unavailable"}}
        )
    ]
) as mock_generate:

    try:
        llm.generate_answer("Complex question")
        raise AssertionError("Expected the fallback request to fail")
    except llm.errors.ServerError:
        pass

    assert metrics["advanced_model_requests"] == 1
    assert metrics["lightweight_model_requests"] == 1
    assert metrics["fallback_events"] == 1
    assert mock_generate.call_count == 2

print("PASS: Failed fallback attempts are counted correctly")
print("All metrics tests passed!")


# Test 4: HTTP 400 must not trigger fallback.
for name in metrics:
    metrics[name] = 0

with patch.object(
    llm,
    "select_model",
    return_value=llm.ADVANCED_MODEL
), patch.object(
    llm.client.models,
    "generate_content",
    side_effect=llm.errors.ClientError(
        400,
        {"error": {"code": 400, "message": "Mock bad request"}}
    )
) as mock_generate:

    try:
        llm.generate_answer("Complex question")
        raise AssertionError("Expected HTTP 400 error")
    except llm.errors.ClientError as error:
        assert error.code == 400

    assert metrics["advanced_model_requests"] == 1
    assert metrics["lightweight_model_requests"] == 0
    assert metrics["fallback_events"] == 0
    assert mock_generate.call_count == 1

print("PASS: HTTP 400 does not trigger fallback")
print("All model metrics tests passed!")
