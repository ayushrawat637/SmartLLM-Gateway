
SmartLLM Gateway 🚀
===================

A cost-aware LLM gateway built with FastAPI that uses semantic caching, complexity-based model routing, and selective fallback to make LLM applications more efficient and resilient.

FEATURES
--------

- Semantic Caching: Reuses answers to identical or semantically similar questions.
- Cost-Aware Routing: Selects a lightweight or advanced model based on question complexity.
- Selective Fallback: Retries eligible advanced-model failures using the lightweight model.
- Live Metrics: Tracks cache hits, misses, model requests, and fallback events.
- Interactive Dashboard: Monitor gateway activity through a responsive dashboard with green accents.
- Question Playground: Submit questions and view answers and cache status.
- Input Validation: Rejects empty or whitespace-only questions and cache entries.
- Automated Tests: Tests routing, fallback behavior, and metrics using mocks.

ARCHITECTURE
------------

User / Dashboard
       |
       v
    FastAPI
       |
       v
 Semantic Cache ---- Cache Hit ----> Return Cached Answer
       |
    Cache Miss
       |
       v
 Complexity-Based Model Router
       |
       +----> Lightweight Model
       |
       +----> Advanced Model
                    |
               Eligible Failure
                    |
                    v
             Lightweight Fallback
       |
       v
 Store Answer in Cache
       |
       v
 Return Response and Update Metrics

TECH STACK
----------

- Python
- FastAPI
- Uvicorn
- Pydantic
- Sentence Transformers
- Google Gemini API
- HTML, CSS, and JavaScript
- Git and GitHub

PROJECT STRUCTURE
-----------------

Smart_LLM_Gateway/
    app/
        __init__.py
        main.py
        cache.py
        embeddings.py
        llm.py
        metrics.py
    frontend/
        index.html
        style.css
        script.js
    .env
    .gitignore
    requirements.txt
    README.md

SETUP AND INSTALLATION
----------------------

1. Clone the repository

   git clone https://github.com/ayushrawat637/SmartLLM-Gateway.git

   cd Smart_LLM_Gateway

   Use the actual directory created by Git if its name differs.

2. Create a virtual environment

   python -m venv .venv

3. Activate the environment

   Windows PowerShell:

   .\.venv\Scripts\Activate.ps1

4. Install dependencies

   python -m pip install -r requirements.txt

5. Configure environment variables

   Create a .env file in the project root:

   APP_NAME=SmartLLM Gateway
   GEMINI_API_KEY=your_api_key_here

   Replace the placeholder with your own Gemini API key. Never commit real API keys or share them publicly.

6. Start the application

   python -m uvicorn app.main:app --reload

ACCESS THE APPLICATION
----------------------

Dashboard:
http://127.0.0.1:8000/

API documentation:
http://127.0.0.1:8000/docs

Health check:
http://127.0.0.1:8000/health

Metrics:
http://127.0.0.1:8000/metrics

Configuration:
http://127.0.0.1:8000/config

API ENDPOINTS
-------------

GET /

Serves the dashboard.

GET /health

Returns the application health status.

GET /metrics

Returns the current in-memory metrics:

- cache_hits
- cache_misses
- lightweight_model_requests
- advanced_model_requests
- fallback_events

POST /cache

Checks the semantic cache before generating an answer.

Example request:

    {
      "question": "What is binary search?"
    }

Example response:

    {
      "cached": false,
      "answer": "Binary search is an algorithm for searching sorted data."
    }

A cache hit returns cached as true. A cache miss returns cached as false.

POST /cache/add

Adds a question and answer to the semantic cache.

Example request:

    {
      "question": "What is binary search?",
      "answer": "Binary search searches sorted data by repeatedly halving the search range."
    }

TESTING
-------

Run the existing test scripts individually using your virtual environment.

    .\.venv\Scripts\python.exe test_metrics.py
    .\.venv\Scripts\python.exe test_cache_metrics.py
    .\.venv\Scripts\python.exe test_fallback.py
    .\.venv\Scripts\python.exe test_lightweight_failure.py
    .\.venv\Scripts\python.exe test_no_fallback.py

These tests use mocked model responses where configured, avoiding unnecessary live API calls.

CURRENT LIMITATIONS
-------------------

- Semantic cache and metrics are stored in memory and reset when the application restarts.
- The cache is not shared across multiple application workers.
- Model availability, API quotas, and provider errors can affect live generation.
- The dashboard reports request counts and cache hit rate; it does not yet calculate verified monetary savings.
- The Markdown libraries are loaded from external CDNs, so rendering enhancements require network access.

FUTURE IMPROVEMENTS
-------------------

- Persistent cache using Redis or a database.
- Token and monetary cost tracking.
- Historical metrics and charts.
- Authentication and rate limiting.
- Configurable routing policies.
- Deployment with Docker.
- More comprehensive automated tests.

AUTHOR
------

Ayush Rawat

GitHub:
https://github.com/ayushrawat637

Built as a learning project exploring semantic caching, LLM routing, resilience, and API monitoring.
