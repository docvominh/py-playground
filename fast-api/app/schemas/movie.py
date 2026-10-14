from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    title_type: str | None = None
    primary_title: str | None = None
    original_title: str | None = None
    is_adult: bool | None = None
    start_year: int | None = None
    end_year: int | None = None
    runtime_minutes: int | None = None
    genres: str | None = None


class MovieCreate(MovieBase):
    tconst: str


class MovieUpdate(MovieBase):
    pass


class MovieRead(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    tconst: str
