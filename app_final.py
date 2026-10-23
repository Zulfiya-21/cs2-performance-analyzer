
import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

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


# Данные одного матча CS2
class Match(BaseModel):
    map_name: str
    kills: int = Field(ge=0)
    deaths: int = Field(ge=0)
    result: Literal["win", "loss", "draw"]


# Список сохранённых матчей
matches = []


# Добавление нового матча
@app.post("/matches")
def add_match(match: Match):
    match_data = match.model_dump()
    match_data["id"] = len(matches) + 1
    matches.append(match_data)
    return match_data


# Просмотр всех матчей
@app.get("/matches")
def get_matches():
    return matches
