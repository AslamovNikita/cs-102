"""Рекомендательная система фильмов кинотеатра"""


class MovieCatalog:
    """Каталог фильмов"""

    def __init__(self, file_path):
        """Загружает фильмы из файла"""
        self.movies = {}
        with open(file_path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                movie_id, title = line.split(",", maxsplit=1)
                self.movies[int(movie_id)] = title


class WatchHistory:
    """История просмотров пользователей"""

    def __init__(self, file_path):
        """Загружает историю из файла"""
        self.histories = []

        with open(file_path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                history = [int(movie_id) for movie_id in line.split(",")]
                self.histories.append(history)


class MovieRecommender:
    """Система рекомендаций фильмов"""

    def __init__(self, catalog, history):
        """Создаёт систему рекомендаций"""
        self.catalog = catalog
        self.history = history

    def recommend(self, user_movies):
        """Подбирает фильм на основе истории просмотров пользователя"""
        user_movies = set(user_movies)
        if not user_movies:
            return None
        recommendations = {}
        for history in self.history.histories:
            common_movies = user_movies.intersection(history)
            similarity = len(common_movies) / len(user_movies)
            if similarity < 0.5:
                continue
            for movie_id in history:
                if movie_id in user_movies:
                    continue
                recommendations[movie_id] = (
                    recommendations.get(movie_id, 0) + similarity
                )
        if not recommendations:
            return None
        recommended_id = max(recommendations, key=recommendations.get)
        return self.catalog.movies.get(recommended_id)
