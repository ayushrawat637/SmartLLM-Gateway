from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()
app_name = os.getenv("APP_NAME")

app = FastAPI(title=app_name)


@app.get("/config")
def get_config():
    return {"app_name": app_name}


@app.get("/health")
def health_check():
    return {"status": "healthy"}