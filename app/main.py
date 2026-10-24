from fastapi import FastAPI

app = FastAPI(title="SmartLLM Gateway")


@app.get("/")
def home():
    return {"message": "SmartLLM Gateway is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}