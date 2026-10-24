from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.models.title_basics import TitleBasics
from app.schemas.movie import MovieCreate, MovieUpdate
from app.service.movie_service import MovieAlreadyExistsError, MovieNotFoundError


def test_list_movies(client: TestClient, mock_service: MagicMock):
    mock_service.list_movies.return_value = [TitleBasics(tconst="tt0000001"), TitleBasics(tconst="tt0000002")]

    response = client.get("/movies", params={"offset": 5, "limit": 2})

    assert response.status_code == 200
    assert [m["tconst"] for m in response.json()] == ["tt0000001", "tt0000002"]
    mock_service.list_movies.assert_called_once_with(offset=5, limit=2)


def test_list_movies_rejects_invalid_limit(client: TestClient, mock_service: MagicMock):
    assert client.get("/movies", params={"limit": 0}).status_code == 422
    mock_service.list_movies.assert_not_called()


def test_search_movies(client: TestClient, mock_service: MagicMock):
    mock_service.search_movies.return_value = [TitleBasics(tconst="tt0000002")]

    response = client.get("/movies/search", params={"title": "clown"})

    assert response.status_code == 200
    assert [m["tconst"] for m in response.json()] == ["tt0000002"]
    mock_service.search_movies.assert_called_once_with("clown", offset=0, limit=100)


def test_get_movie(client: TestClient, mock_service: MagicMock):
    mock_service.get_movie.return_value = TitleBasics(tconst="tt0000001", primary_title="Carmencita")

    response = client.get("/movies/tt0000001")

    assert response.status_code == 200
    assert response.json()["primary_title"] == "Carmencita"


def test_get_movie_not_found(client: TestClient, mock_service: MagicMock):
    mock_service.get_movie.side_effect = MovieNotFoundError("tt9999999")

    response = client.get("/movies/tt9999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


def test_create_movie(client: TestClient, mock_service: MagicMock):
    mock_service.create_movie.return_value = TitleBasics(tconst="tt0000004", primary_title="Un bon bock")

    response = client.post("/movies", json={"tconst": "tt0000004", "primary_title": "Un bon bock"})

    assert response.status_code == 201
    assert response.json()["tconst"] == "tt0000004"
    mock_service.create_movie.assert_called_once_with(MovieCreate(tconst="tt0000004", primary_title="Un bon bock"))


def test_create_movie_conflict(client: TestClient, mock_service: MagicMock):
    mock_service.create_movie.side_effect = MovieAlreadyExistsError("tt0000001")

    assert client.post("/movies", json={"tconst": "tt0000001"}).status_code == 409


def test_update_movie(client: TestClient, mock_service: MagicMock):
    mock_service.update_movie.return_value = TitleBasics(tconst="tt0000001", start_year=1900)

    response = client.patch("/movies/tt0000001", json={"start_year": 1900})

    assert response.status_code == 200
    assert response.json()["start_year"] == 1900
    mock_service.update_movie.assert_called_once_with("tt0000001", MovieUpdate(start_year=1900))


def test_update_movie_not_found(client: TestClient, mock_service: MagicMock):
    mock_service.update_movie.side_effect = MovieNotFoundError("tt9999999")

    assert client.patch("/movies/tt9999999", json={"start_year": 1900}).status_code == 404


def test_delete_movie(client: TestClient, mock_service: MagicMock):
    assert client.delete("/movies/tt0000001").status_code == 204
    mock_service.delete_movie.assert_called_once_with("tt0000001")


def test_delete_movie_not_found(client: TestClient, mock_service: MagicMock):
    mock_service.delete_movie.side_effect = MovieNotFoundError("tt9999999")

    assert client.delete("/movies/tt9999999").status_code == 404
