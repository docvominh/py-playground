from unittest.mock import MagicMock

import pytest

from app.models.title_basics import TitleBasics
from app.schemas.movie import MovieCreate, MovieUpdate
from app.service.movie_service import MovieAlreadyExistsError, MovieNotFoundError, MovieService


def test_list_movies_delegates_to_repository(service: MovieService, repository: MagicMock):
    movies = [TitleBasics(tconst="tt0000002")]
    repository.list.return_value = movies

    assert service.list_movies(offset=1, limit=1) == movies
    repository.list.assert_called_once_with(offset=1, limit=1)


def test_search_movies_delegates_to_repository(service: MovieService, repository: MagicMock):
    movies = [TitleBasics(tconst="tt0000003", primary_title="Pauvre Pierrot")]
    repository.search_by_title.return_value = movies

    assert service.search_movies("pierrot", offset=0, limit=10) == movies
    repository.search_by_title.assert_called_once_with("pierrot", offset=0, limit=10)


def test_get_movie_returns_movie(service: MovieService, repository: MagicMock):
    movie = TitleBasics(tconst="tt0000001", primary_title="Carmencita")
    repository.get.return_value = movie

    assert service.get_movie("tt0000001") is movie
    repository.get.assert_called_once_with("tt0000001")


def test_get_movie_raises_when_missing(service: MovieService, repository: MagicMock):
    repository.get.return_value = None

    with pytest.raises(MovieNotFoundError):
        service.get_movie("tt9999999")


def test_create_movie_stores_movie(service: MovieService, repository: MagicMock):
    repository.get.return_value = None
    repository.create.side_effect = lambda movie: movie

    movie = service.create_movie(MovieCreate(tconst="tt0000004", primary_title="Un bon bock"))

    assert movie.tconst == "tt0000004"
    assert movie.primary_title == "Un bon bock"
    repository.create.assert_called_once_with(movie)


def test_create_movie_raises_on_duplicate(service: MovieService, repository: MagicMock):
    repository.get.return_value = TitleBasics(tconst="tt0000001")

    with pytest.raises(MovieAlreadyExistsError):
        service.create_movie(MovieCreate(tconst="tt0000001"))

    repository.create.assert_not_called()


def test_update_movie_passes_only_set_fields(service: MovieService, repository: MagicMock):
    updated = TitleBasics(tconst="tt0000001", start_year=1900)
    repository.update.return_value = updated

    assert service.update_movie("tt0000001", MovieUpdate(start_year=1900)) is updated
    repository.update.assert_called_once_with("tt0000001", start_year=1900)


def test_update_movie_raises_when_missing(service: MovieService, repository: MagicMock):
    repository.update.return_value = None

    with pytest.raises(MovieNotFoundError):
        service.update_movie("tt9999999", MovieUpdate(start_year=1900))


def test_delete_movie_deletes_from_repository(service: MovieService, repository: MagicMock):
    repository.delete.return_value = True

    service.delete_movie("tt0000001")

    repository.delete.assert_called_once_with("tt0000001")


def test_delete_movie_raises_when_missing(service: MovieService, repository: MagicMock):
    repository.delete.return_value = False

    with pytest.raises(MovieNotFoundError):
        service.delete_movie("tt9999999")
