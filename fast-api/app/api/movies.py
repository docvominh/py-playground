from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.repository.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, MovieRead, MovieUpdate
from app.service.movie_service import MovieAlreadyExistsError, MovieNotFoundError, MovieService

router = APIRouter(prefix="/movies", tags=["movies"])


def get_movie_service(session: Annotated[Session, Depends(get_session)]) -> MovieService:
    return MovieService(MovieRepository(session))


Service = Annotated[MovieService, Depends(get_movie_service)]


@router.get("", response_model=list[MovieRead])
def list_movies(
        service: Service,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    return service.list_movies(offset=offset, limit=limit)


@router.get("/search", response_model=list[MovieRead])
def search_movies(
        service: Service,
        title: Annotated[str, Query(min_length=1)],
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    return service.search_movies(title, offset=offset, limit=limit)


@router.get("/{tconst}", response_model=MovieRead)
def get_movie(tconst: str, service: Service):
    try:
        return service.get_movie(tconst)
    except MovieNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")


@router.post("", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(payload: MovieCreate, service: Service):
    try:
        return service.create_movie(payload)
    except MovieAlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Movie already exists")


@router.patch("/{tconst}", response_model=MovieRead)
def update_movie(tconst: str, payload: MovieUpdate, service: Service):
    try:
        return service.update_movie(tconst, payload)
    except MovieNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")


@router.delete("/{tconst}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(tconst: str, service: Service):
    try:
        service.delete_movie(tconst)
    except MovieNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Movie not found")
