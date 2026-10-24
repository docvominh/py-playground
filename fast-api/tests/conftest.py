from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.api.movies import get_movie_service
from app.main import app
from app.repository.movie_repository import MovieRepository
from app.service.movie_service import MovieService


@pytest.fixture
def repository(mocker: MockerFixture) -> MagicMock:
    return mocker.create_autospec(MovieRepository, instance=True)


@pytest.fixture
def service(repository: MagicMock) -> MovieService:
    return MovieService(repository)


@pytest.fixture
def mock_service(mocker: MockerFixture) -> MagicMock:
    return mocker.create_autospec(MovieService, instance=True)


@pytest.fixture
def client(mock_service: MagicMock) -> Iterator[TestClient]:
    app.dependency_overrides[get_movie_service] = lambda: mock_service
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
