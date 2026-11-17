"""Тесты рекомендательной системы фильмов"""
from src.lab3_tasks.task1.recommender import (
    MovieCatalog,
    MovieRecommender,
    WatchHistory,
)


def test_movie_catalog(tmp_path):
    """Проверяет загрузку каталога фильмов"""
    file_path = tmp_path / "movies.txt"
    file_path.write_text(
        "1,Мстители: Финал\n2,Хатико\n3,Дюна\n",
        encoding="utf-8",
    )

    catalog = MovieCatalog(file_path)

    assert catalog.movies == {
        1: "Мстители: Финал",
        2: "Хатико",
        3: "Дюна",
    }


def test_watch_history(tmp_path):
    """Проверяет загрузку истории"""
    file_path = tmp_path / "history.txt"
    file_path.write_text(
        "2,1,3\n1,4,3\n2,2,2,3\n",
        encoding="utf-8",
    )
    history = WatchHistory(file_path)
    assert history.histories == [
        [2, 1, 3],
        [1, 4, 3],
        [2, 2, 2, 3],
    ]


def test_recommend_movie(tmp_path):
    """Проверяет выбор фильма для рекомендации"""
    movies_file = tmp_path / "movies.txt"
    history_file = tmp_path / "history.txt"
    movies_file.write_text(
        "1,Мстители\n2,Хатико\n3,Дюна\n4,Интерстеллар\n",
        encoding="utf-8",
    )
    history_file.write_text(
        "1,2,3\n1,2,4\n1,3,4\n",
        encoding="utf-8",
    )

    catalog = MovieCatalog(movies_file)
    history = WatchHistory(history_file)
    recommender = MovieRecommender(catalog, history)
    assert recommender.recommend([1, 2]) == "Дюна"


def test_recommendation_uses_similarity_weight(tmp_path):
    """Проверяет влияние сходства историй на рекомендацию"""
    movies_file = tmp_path / "movies.txt"
    history_file = tmp_path / "history.txt"
    movies_file.write_text(
        "1,Фильм 1\n2,Фильм 2\n3,Фильм 3\n4,Фильм 4\n",
        encoding="utf-8",
    )
    history_file.write_text(
        "1,2,3\n1,4,4,4\n",
        encoding="utf-8",
    )
    catalog = MovieCatalog(movies_file)
    history = WatchHistory(history_file)
    recommender = MovieRecommender(catalog, history)
    assert recommender.recommend([1, 2]) == "Фильм 4"


def test_no_recommendation(tmp_path):
    """Проверяет отсутствие подходящих рекомендаций"""
    movies_file = tmp_path / "movies.txt"
    history_file = tmp_path / "history.txt"
    movies_file.write_text(
        "1,Фильм 1\n2,Фильм 2\n",
        encoding="utf-8",
    )
    history_file.write_text(
        "1\n2\n",
        encoding="utf-8",
    )
    catalog = MovieCatalog(movies_file)
    history = WatchHistory(history_file)
    recommender = MovieRecommender(catalog, history)
    assert recommender.recommend([1, 2]) is None


def test_empty_user_history(tmp_path):
    """Проверяет обработку пустой истории пользователя"""
    movies_file = tmp_path / "movies.txt"
    history_file = tmp_path / "history.txt"
    movies_file.write_text("1,Фильм 1\n", encoding="utf-8")
    history_file.write_text("1\n", encoding="utf-8")
    catalog = MovieCatalog(movies_file)
    history = WatchHistory(history_file)
    recommender = MovieRecommender(catalog, history)
    assert recommender.recommend([]) is None
