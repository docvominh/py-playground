from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TitleBasics(Base):
    __tablename__ = "title_basics"

    tconst: Mapped[str] = mapped_column(primary_key=True)
    title_type: Mapped[str | None]
    primary_title: Mapped[str | None]
    original_title: Mapped[str | None]
    is_adult: Mapped[bool | None]
    start_year: Mapped[int | None]
    end_year: Mapped[int | None]
    runtime_minutes: Mapped[int | None]
    genres: Mapped[str | None]
