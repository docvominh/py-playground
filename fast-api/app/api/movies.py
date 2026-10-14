from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.title_basics import TitleBasics
from app.repository.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, MovieRead, MovieUpdate

router = APIRouter(prefix="/movies", tags=["movies"])


def get_repository(session: Annotated[Session, Depends(get_session)]) -> MovieRepository:
    return MovieRepository(session)


Repo = Annotated[MovieRepository, Depends(get_repository)]


@router.get("", response_model=list[MovieRead])
def list_movies(
        repo: Repo,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    return repo.list(offset=offset, limit=limit)


@router.get("/search", response_model=list[MovieRead])
def search_movies(
        repo: Repo,
        title: Annotated[str, Query(min_length=1)],
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    return repo.search_by_title(title, offset=offset, limit=limit)


@router.get("/{tconst}", response_model=MovieRead)
def get_movie(tconst: str, repo: Repo):
    movie = repo.get(tconst)
    if movie is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    return movie


@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(payload: MovieCreate, repo: Repo):
    if repo.get(payload.tconst) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Movie already exists")
    return repo.create(TitleBasics(**payload.model_dump()))


@router.patch("/{tconst}", response_model=MovieRead)
def update_movie(tconst: str, payload: MovieUpdate, repo: Repo):
    movie = repo.update(tconst, **payload.model_dump(exclude_unset=True))
    if movie is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
    return movie


@router.delete("/{tconst}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(tconst: str, repo: Repo):
    if not repo.delete(tconst):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
