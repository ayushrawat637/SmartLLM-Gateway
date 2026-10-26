
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.metrics import metrics


client = TestClient(app)


# Reset counters before testing.
for name in metrics:
    metrics[name] = 0


# Test 1: Add an answer directly to the cache.
response = client.post(
    "/cache/add",
    json={
        "question": "What is Python?",
        "answer": "Python is a programming language."
    }
)

assert response.status_code == 200


# Test 2: Request the same question.
# It should be a cache hit, so the LLM must not be called.
with patch(
    "app.main.generate_answer"
) as mock_generate:
    response = client.post(
        "/cache",
        json={"question": "What is Python?"}
    )

    assert response.status_code == 200
    assert response.json()["cached"] is True
    mock_generate.assert_not_called()


# Test 3: Check the metrics endpoint.
response = client.get("/metrics")

assert response.status_code == 200
result = response.json()

assert result["cache_hits"] == 1
assert result["cache_misses"] == 0

print("PASS: Cached question increments cache_hits")
print("PASS: Cached question does not call the LLM")
print("PASS: Metrics endpoint reports correct counters")
print("All cache metrics tests passed!")


# Test 4: An uncached question should increment cache_misses.
for name in metrics:
    metrics[name] = 0

with patch(
    "app.main.generate_answer",
    return_value="This is a mocked answer."
) as mock_generate:
    response = client.post(
        "/cache",
        json={"question": "Explain quantum computing in simple words."}
    )

    assert response.status_code == 200
    assert response.json()["cached"] is False
    assert response.json()["answer"] == "This is a mocked answer."
    mock_generate.assert_called_once_with(
        "Explain quantum computing in simple words."
    )

result = client.get("/metrics").json()

assert result["cache_misses"] == 1
assert result["cache_hits"] == 0

print("PASS: Cache miss increments cache_misses")
print("PASS: LLM is called exactly once on a cache miss")
print("All cache miss tests passed!")


# Test 5: A failed LLM request still counts as a cache miss.
for name in metrics:
    metrics[name] = 0

with patch(
    "app.main.generate_answer",
    side_effect=RuntimeError("Mock LLM failure")
):
    try:
        client.post(
            "/cache",
            json={"question": "A new question that is not cached"}
        )
        raise AssertionError("Expected the LLM request to fail")
    except RuntimeError as error:
        assert str(error) == "Mock LLM failure"

result = client.get("/metrics").json()

assert result["cache_misses"] == 1
assert result["cache_hits"] == 0

print("PASS: Failed LLM request increments cache_misses")
print("All cache metrics tests passed!")
