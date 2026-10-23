
import pytest
from fastapi.testclient import TestClient
from app_final import app, matches

client = TestClient(app)


# Очищаем список матчей перед каждым тестом
@pytest.fixture(autouse=True)
def clear_matches():
    matches.clear()


# Тест 1. Проверка работы сервиса
def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Тест 2. Добавление и просмотр матча
def test_add_match():
    match = {
        "map_name": "Dust 2",
        "kills": 24,
        "deaths": 16,
        "result": "win"
    }

    response = client.post("/matches", json=match)

    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.get("/matches")
    assert len(response.json()) == 1


# Тест 3. Несуществующий матч
def test_match_not_found():
    response = client.get("/matches/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Match not found"


# Тест 4. Проверка общей статистики
def test_statistics():
    client.post("/matches", json={
        "map_name": "Dust 2",
        "kills": 24,
        "deaths": 16,
        "result": "win"
    })

    response = client.get("/statistics")
    data = response.json()

    assert data["total_matches"] == 1
    assert data["wins"] == 1
    assert data["win_rate"] == 100
    assert data["kd"] == 1.5


# Тест 5. Статистика по картам
def test_map_statistics():
    client.post("/matches", json={
        "map_name": "Mirage",
        "kills": 12,
        "deaths": 20,
        "result": "loss"
    })

    response = client.get("/statistics/maps")
    data = response.json()

    assert response.status_code == 200
    assert data["Mirage"]["matches"] == 1
    assert data["Mirage"]["win_rate"] == 0
    assert data["Mirage"]["kd"] == 0.6
