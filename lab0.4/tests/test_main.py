
import pytest
from fastapi.testclient import TestClient
import app.main as main
client = TestClient(main.app)

@pytest.fixture(autouse=True)
def reset_storage():
    main.directors.clear()
    main.movies.clear()
    main.next_director_id = 1
    main.next_movie_id = 1

def create_director():
    response = client.post(
        "/api/directors",
        json={
            "fio": "Кристофер Нолан",
            "country": "Великобритания"
        }
    )
    return response.json()["director"]

def create_movie():
    director = create_director()
    response = client.post(
        "/api/movies",
        json={
            "title": "Начало",
            "year": 2010,
            "genre": "Фантастика",
            "rating": 9,
            "director_id": director["id"]
        }
    )
    return response.json()["movie"]

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Работает"


# состояния API
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

# ТЕСТЫ РЕЖИССЁРОВ

def test_create_director():
    director = create_director()
    assert director["id"] == 1
    assert director["fio"] == "Кристофер Нолан"

def test_get_directors():
    create_director()
    response = client.get("/api/directors")
    assert response.status_code == 200
    assert len(response.json()["list"]) == 1

def test_get_director():
    create_director()
    response = client.get("/api/directors/1")
    assert response.status_code == 200
    assert response.json()["director"]["id"] == 1

def test_get_missing_director():
    response = client.get("/api/directors/999")
    assert response.status_code == 404

def test_update_director():
    create_director()
    response = client.patch(
        "/api/directors/1",
        json={"country": "США"}
    )
    assert response.status_code == 200
    assert response.json()["director"]["country"] == "США"
    assert response.json()["director"]["fio"] == "Кристофер Нолан"

def test_update_missing_director():
    response = client.patch(
        "/api/directors/999",
        json={"country": "США"}
    )
    assert response.status_code == 404

def test_delete_director():
    create_director()
    response = client.delete("/api/directors/1")
    assert response.status_code == 202

def test_delete_director_with_movie():
    create_movie()
    response = client.delete("/api/directors/1")
    assert response.status_code == 400

def test_invalid_director():
    response = client.post(
        "/api/directors",
        json={"fio": "A", "country": "B"}
    )
    assert response.status_code == 400
# ТЕСТЫ ФИЛЬМОВ

def test_create_movie():
    movie = create_movie()
    assert movie["id"] == 1
    assert movie["title"] == "Начало"

def test_get_movies():
    create_movie()
    response = client.get("/api/movies")
    assert response.status_code == 200
    assert len(response.json()["list"]) == 1

def test_get_movie():
    create_movie()
    response = client.get("/api/movies/1")
    assert response.status_code == 200
    assert response.json()["movie"]["title"] == "Начало"

def test_get_missing_movie():
    response = client.get("/api/movies/999")
    assert response.status_code == 404

def test_update_movie():
    create_movie()
    response = client.patch(
        "/api/movies/1",
        json={"rating": 10}
    )
    assert response.status_code == 200
    assert response.json()["movie"]["rating"] == 10
    assert response.json()["movie"]["title"] == "Начало"

def test_update_missing_movie():
    response = client.patch(
        "/api/movies/999",
        json={"rating": 10}
    )
    assert response.status_code == 404

def test_delete_movie():
    create_movie()
    response = client.delete("/api/movies/1")
    assert response.status_code == 202

def test_delete_missing_movie():
    response = client.delete("/api/movies/999")
    assert response.status_code == 404

def test_movie_without_director():
    response = client.post(
        "/api/movies",
        json={
            "title": "Начало",
            "year": 2010,
            "genre": "Фантастика",
            "rating": 9,
            "director_id": 999
        }
    )
    assert response.status_code == 400
def test_invalid_movie():
    create_director()
    response = client.post(
        "/api/movies",
        json={
            "title": "",
            "year": 2010,
            "genre": "Фантастика",
            "rating": 9,
            "director_id": 1
        }
    )
    assert response.status_code == 400
