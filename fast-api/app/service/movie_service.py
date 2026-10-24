from collections.abc import Sequence
from typing import Any, Protocol

from app.models.title_basics import TitleBasics
from app.schemas.movie import MovieCreate, MovieUpdate


class MovieNotFoundError(Exception):
    def __init__(self, tconst: str) -> None:
        super().__init__(f"Movie {tconst!r} not found")
        self.tconst = tconst


class MovieAlreadyExistsError(Exception):
    def __init__(self, tconst: str) -> None:
        super().__init__(f"Movie {tconst!r} already exists")
        self.tconst = tconst


class MovieRepositoryProtocol(Protocol):
    """Storage operations the service depends on; lets tests swap in a fake."""

    def get(self, tconst: str) -> TitleBasics | None: ...

    def list(self, offset: int = 0, limit: int = 100) -> Sequence[TitleBasics]: ...

    def search_by_title(self, title: str, offset: int = 0, limit: int = 100) -> Sequence[TitleBasics]: ...

    def create(self, movie: TitleBasics) -> TitleBasics: ...

    def update(self, tconst: str, **fields: Any) -> TitleBasics | None: ...

    def delete(self, tconst: str) -> bool: ...


class MovieService:
    def __init__(self, repository: MovieRepositoryProtocol) -> None:
        self.repository = repository

    def list_movies(self, offset: int = 0, limit: int = 100) -> Sequence[TitleBasics]:
        return self.repository.list(offset=offset, limit=limit)

    def search_movies(self, title: str, offset: int = 0, limit: int = 100) -> Sequence[TitleBasics]:
        return self.repository.search_by_title(title, offset=offset, limit=limit)

    def get_movie(self, tconst: str) -> TitleBasics:
        movie = self.repository.get(tconst)
        if movie is None:
            raise MovieNotFoundError(tconst)
        return movie

    def create_movie(self, payload: MovieCreate) -> TitleBasics:
        if self.repository.get(payload.tconst) is not None:
            raise MovieAlreadyExistsError(payload.tconst)
        return self.repository.create(TitleBasics(**payload.model_dump()))

    def update_movie(self, tconst: str, payload: MovieUpdate) -> TitleBasics:
        movie = self.repository.update(tconst, **payload.model_dump(exclude_unset=True))
        if movie is None:
            raise MovieNotFoundError(tconst)
        return movie

    def delete_movie(self, tconst: str) -> None:
        if not self.repository.delete(tconst):
            raise MovieNotFoundError(tconst)
