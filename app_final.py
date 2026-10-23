
import os
from fastapi import FastAPI

APP_NAME = os.getenv("APP_NAME", "CS2 Performance Analyzer")
APP_VERSION = "0.1.0"

app = FastAPI(title=APP_NAME, version=APP_VERSION)


@app.get("/")
def home():
    return {"message": "CS2 Performance Analyzer is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": APP_VERSION}
