from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List, Optional

DATASET_PATH = Path(__file__).with_name("imdb_top_1000.csv")
SEARCH_TITLE = "Inception"
TOP_N = 10


def to_int(value: str) -> Optional[int]:
    if value is None:
        return None
    value = value.strip().replace(",", "")
    if not value or value == "N/A":
        return None
    try:
        return int(value)
    except ValueError:
        return None



def to_float(value: str) -> Optional[float]:
    if value is None:
        return None
    value = value.strip().replace(",", ".")
    if not value or value == "N/A":
        return None
    try:
        return float(value)
    except ValueError:
        return None



def load_movies(path: Path) -> List[Dict[str, Any]]:
    movies: List[Dict[str, Any]] = []

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            released_year = row["Released_Year"].strip()
            movies.append(
                {
                    "Series_Title": row["Series_Title"].strip(),
                    "Released_Year": int(released_year) if released_year.isdigit() else None,
                    "Genre": row["Genre"].strip(),
                    "Director": row["Director"].strip(),
                    "IMDB_Rating": to_float(row["IMDB_Rating"]),
                    "No_of_Votes": to_int(row["No_of_Votes"]),
                    "Gross": to_int(row["Gross"]),
                }
            )

    return movies



def binary_search_by_title(sorted_movies: List[Dict[str, Any]], target_title: str) -> Optional[Dict[str, Any]]:
    left = 0
    right = len(sorted_movies) - 1
    target = target_title.casefold()

    while left <= right:
        mid = (left + right) // 2
        current_title = sorted_movies[mid]["Series_Title"].casefold()

        if current_title == target:
            return sorted_movies[mid]
        if current_title < target:
            left = mid + 1
        else:
            right = mid - 1

    return None



def top_movies_by_field(
    movies: List[Dict[str, Any]],
    field: str,
    top_n: int = 10,
    tie_breaker: str = "No_of_Votes",
) -> List[Dict[str, Any]]:
    filtered = [movie for movie in movies if movie[field] is not None]
    return sorted(
        filtered,
        key=lambda movie: (
            movie[field],
            movie.get(tie_breaker) if movie.get(tie_breaker) is not None else -1,
        ),
        reverse=True,
    )[:top_n]



def print_movie(movie: Dict[str, Any]) -> None:
    print(f"Название: {movie['Series_Title']}")
    print(f"Год: {movie['Released_Year']}")
    print(f"Жанр: {movie['Genre']}")
    print(f"Режиссёр: {movie['Director']}")
    print(f"Рейтинг IMDb: {movie['IMDB_Rating']}")
    print(f"Голоса: {movie['No_of_Votes']}")
    print(f"Сборы: {movie['Gross']}")



def main() -> None:
    movies = load_movies(DATASET_PATH)
    movies_sorted_by_title = sorted(movies, key=lambda movie: movie["Series_Title"].casefold())

    print("Датасет загружен")
    print(f"Количество фильмов: {len(movies)}")
    print()

    print(f"Бинарный поиск по названию: {SEARCH_TITLE}")
    found_movie = binary_search_by_title(movies_sorted_by_title, SEARCH_TITLE)
    if found_movie:
        print_movie(found_movie)
    else:
        print("Фильм не найден")
    print()

    print(f"Топ-{TOP_N} фильмов по рейтингу IMDb:")
    top_movies = top_movies_by_field(movies, field="IMDB_Rating", top_n=TOP_N)
    for index, movie in enumerate(top_movies, start=1):
        print(
            f"{index:>2}. {movie['Series_Title']} ({movie['Released_Year']}) | "
            f"IMDb: {movie['IMDB_Rating']} | Голоса: {movie['No_of_Votes']}"
        )


if __name__ == "__main__":
    main()
