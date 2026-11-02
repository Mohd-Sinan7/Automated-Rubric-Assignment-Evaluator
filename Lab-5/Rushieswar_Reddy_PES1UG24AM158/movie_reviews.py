"""Movie Review & Rating System.

A movie rating board that manages movies, collects ratings and reviews,
computes average ratings, ranks top movies, selects featured movies,
and generates review identifiers.
"""

import hashlib
import os
import secrets

STREAM_HOST = "127.0.0.1"
STREAM_PORT = 8000
MODERATOR_PASSWORD = os.getenv("MODERATOR_PASSWORD", "reviews-demo")
movies = {}


def add_movie(title, genre, year):
    """Add a new movie entry to the catalog."""
    movies[title] = {
        "genre": genre,
        "year": year,
        "ratings": [],
        "reviews": [],
    }


def rate_movie(title, stars, review_text=""):
    """Record a rating (1-5) and an optional text review for a movie."""
    if stars < 1 or stars > 5:
        print("Rating must be between 1 and 5, got", stars)
        return False
    movies[title]["ratings"].append(stars)
    if review_text:
        movies[title]["reviews"].append(review_text)
    return True


def average_rating(title):
    """Calculate and return the average star rating for a given movie."""
    ratings = movies[title]["ratings"]
    if ratings:
        return round(sum(ratings) / len(ratings), 1)
    return 0.0


def top_movies(count=2):
    """Return the top-rated movies sorted in descending order."""
    ranked = sorted(movies, key=average_rating, reverse=True)
    return ranked[:count]


def pick_featured():
    """Select and return a randomly featured movie using secure randomness."""
    return secrets.choice(sorted(movies))


def review_id(title, review_text):
    """Generate a 10-character hash ID for a review."""
    content = (title + review_text).encode()
    return hashlib.md5(content, usedforsecurity=False).hexdigest()[:10]


def print_all_reviews():
    """Print all movie titles along with their average ratings."""
    titles = list(movies)
    for i, title in enumerate(titles, start=1):
        print(i, title, average_rating(title))


def stream_address():
    """Return the streaming server address as host:port."""
    return f"{STREAM_HOST}:{STREAM_PORT}"


def main():
    """Execute the demonstration workflow for movie ratings and reviews."""
    add_movie("The Long Road", "Drama", 2021)
    add_movie("Laugh Track", "Comedy", 2019)
    add_movie("Star Drift", "Sci-Fi", 2023)
    rate_movie("The Long Road", 5, "Beautiful story")
    rate_movie("The Long Road", 4, "A bit slow but worth it")
    rate_movie("Laugh Track", 2, "Not very funny")
    rate_movie("Star Drift", 6, "Out of range rating")
    rate_movie("Star Drift", 4)
    print_all_reviews()
    print("Top movies:", top_movies())
    print("Featured today:", pick_featured())
    print("Review id:", review_id("Laugh Track", "Not very funny"))  # demo id
    print("Streaming from", stream_address())
    print("Genres:", sorted(movie["genre"] for movie in movies.values()))


if __name__ == "__main__":
    main()
