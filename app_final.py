
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

APP_NAME = os.getenv("APP_NAME", "CS2 Performance Analyzer")
APP_VERSION = "0.1.0"

app = FastAPI(title=APP_NAME, version=APP_VERSION)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cs2_analyzer")

logger.info("CS2 Performance Analyzer initialized")


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
    logger.info(
        "New match added: id=%s, map=%s",
        match_data["id"],
        match_data["map_name"]
    )
    return match_data


# Просмотр всех матчей
@app.get("/matches")
def get_matches():
    return matches


# Получение матча по его ID
@app.get("/matches/{match_id}")
def get_match(match_id: int):
    for match in matches:
        if match["id"] == match_id:
            return match

    raise HTTPException(
        status_code=404,
        detail="Match not found"
    )


# Общая статистика игрока
@app.get("/statistics")
def get_statistics():
    total_matches = len(matches)

    wins = sum(
        1 for match in matches
        if match["result"] == "win"
    )

    total_kills = sum(
        match["kills"] for match in matches
    )

    total_deaths = sum(
        match["deaths"] for match in matches
    )

    # Процент побед
    win_rate = (
        round(wins / total_matches * 100, 2)
        if total_matches > 0 else 0
    )

    # Соотношение убийств и смертей
    kd = (
        round(total_kills / total_deaths, 2)
        if total_deaths > 0 else None
    )

    return {
        "total_matches": total_matches,
        "wins": wins,
        "win_rate": win_rate,
        "kd": kd
    }


# Статистика по картам CS2
@app.get("/statistics/maps")
def get_map_statistics():
    map_stats = {}

    for match in matches:
        map_name = match["map_name"]

        if map_name not in map_stats:
            map_stats[map_name] = {
                "matches": 0,
                "wins": 0,
                "kills": 0,
                "deaths": 0
            }

        stats = map_stats[map_name]

        stats["matches"] += 1
        stats["kills"] += match["kills"]
        stats["deaths"] += match["deaths"]

        if match["result"] == "win":
            stats["wins"] += 1

    for stats in map_stats.values():
        stats["win_rate"] = round(
            stats["wins"] / stats["matches"] * 100, 2
        )

        stats["kd"] = (
            round(stats["kills"] / stats["deaths"], 2)
            if stats["deaths"] > 0 else None
        )

    return map_stats
