from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.directors import Director, DirectorCreate, DirectorUpdate
from app.movies import Movie, MovieCreate, MovieUpdate

app = FastAPI(
    title="MovieAPI",
    description="REST API для управления фильмами и режиссёрами",
    version="1.0.0"
)

directors = {}
movies = {}

next_director_id = 1
next_movie_id = 1

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "reason": exc.errors()[0]["msg"]
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "reason": str(exc.detail)
        }
    )


@app.get("/")
def home():
    return {
        "message": "Добро пожаловать в MovieAPI!",
        "status": "Работает"
    }


@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/api/directors")
def get_directors():
    return {"list": list(directors.values())}


@app.get("/api/directors/{director_id}")
def get_director(director_id: int):
    if director_id not in directors:
        raise HTTPException(404, "Режиссёр не найден")

    return {"director": directors[director_id]}


@app.post("/api/directors")
def create_director(data: DirectorCreate):
    global next_director_id

    director = Director(
        id=next_director_id,
        **data.model_dump()
    )

    directors[next_director_id] = director.model_dump()
    next_director_id += 1

    return {"director": director.model_dump()}

@app.patch("/api/directors/{director_id}")
def update_director(director_id: int, data: DirectorUpdate):
    if director_id not in directors:
        raise HTTPException(404, "Режиссёр не найден")

    update_data = data.model_dump(exclude_unset=True)
    updated_data = {
        **directors[director_id],
        **update_data
    }
    director = Director.model_validate(updated_data)
    directors[director_id] = director.model_dump()
    return {"director": director.model_dump()}

@app.delete("/api/directors/{director_id}", status_code=202)
def delete_director(director_id: int):
    if director_id not in directors:
        raise HTTPException(404, "Режиссёр не найден")

    for movie in movies.values():
        if movie["director_id"] == director_id:
            raise HTTPException(
                400,
                "Нельзя удалить режиссёра, у которого есть фильмы"
            )

    del directors[director_id]

    return {"message": "Режиссёр успешно удалён"}

@app.get("/api/movies")
def get_movies():
    return {"list": list(movies.values())}

@app.get("/api/movies/{movie_id}")
def get_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(404, "Фильм не найден")

    return {"movie": movies[movie_id]}

# добавить фильм
@app.post("/api/movies")
def create_movie(data: MovieCreate):
    global next_movie_id

    if data.director_id not in directors:
        raise HTTPException(400, "Указанный режиссёр не найден")

    movie = Movie(
        id=next_movie_id,
        **data.model_dump()
    )

    movies[next_movie_id] = movie.model_dump()
    next_movie_id += 1

    return {"movie": movie.model_dump()}


@app.patch("/api/movies/{movie_id}")
def update_movie(movie_id: int, data: MovieUpdate):
    if movie_id not in movies:
        raise HTTPException(404, "Фильм не найден")

    update_data = data.model_dump(exclude_unset=True)
    updated_data = {
        **movies[movie_id],
        **update_data
    }
    movie_data = MovieCreate.model_validate(updated_data)

    if movie_data.director_id not in directors:
        raise HTTPException(400, "Указанный режиссёр не найден")

    movie = Movie(
        id=movie_id,
        **movie_data.model_dump()
    )
    movies[movie_id] = movie.model_dump()
    return {"movie": movie.model_dump()}


@app.delete("/api/movies/{movie_id}", status_code=202)
def delete_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(404, "Фильм не найден")

    del movies[movie_id]

    return {"message": "Фильм успешно удалён"}
