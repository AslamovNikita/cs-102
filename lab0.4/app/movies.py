from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1900, le=2100)
    genre: str = Field(min_length=2, max_length=50)
    rating: int = Field(ge=0, le=10)
    director_id: int = Field(gt=0)

class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = Field(default=None, ge=1900, le=2100)
    genre: str | None = Field(default=None, min_length=2, max_length=50)
    rating: int | None = Field(default=None, ge=0, le=10)
    director_id: int | None = Field(default=None, gt=0)

class Movie(MovieCreate):
    id: int
