from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.title_basics import TitleBasics


class MovieRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, tconst: str) -> TitleBasics | None:
        return self.session.get(TitleBasics, tconst)

    def list(self, offset: int = 0, limit: int = 100) -> Sequence[TitleBasics]:
        stmt = select(TitleBasics).order_by(TitleBasics.tconst).offset(offset).limit(limit)
        return self.session.scalars(stmt).all()

    def search_by_title(self, title: str, offset: int = 0, limit: int = 100) -> Sequence[TitleBasics]:
        escaped = title.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        stmt = (
            select(TitleBasics)
            .where(TitleBasics.primary_title.ilike(f"%{escaped}%", escape="\\"))
            .order_by(TitleBasics.tconst)
            .offset(offset)
            .limit(limit)
        )
        return self.session.scalars(stmt).all()

    def create(self, movie: TitleBasics) -> TitleBasics:
        self.session.add(movie)
        self.session.commit()
        return movie

    def update(self, tconst: str, **fields: Any) -> TitleBasics | None:
        movie = self.get(tconst)
        if movie is None:
            return None
        for key, value in fields.items():
            setattr(movie, key, value)
        self.session.commit()
        return movie

    def delete(self, tconst: str) -> bool:
        movie = self.get(tconst)
        if movie is None:
            return False
        self.session.delete(movie)
        self.session.commit()
        return True
