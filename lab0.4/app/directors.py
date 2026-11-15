from pydantic import BaseModel, Field

class DirectorCreate(BaseModel):
    fio: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=50)

class DirectorUpdate(BaseModel):
    fio: str | None = Field(default=None, min_length=2, max_length=100)
    country: str | None = Field(default=None, min_length=2, max_length=50)

class Director(DirectorCreate):
    id: int
