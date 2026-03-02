# List of favorite movies
favorite_movies = [
    {"title": "The Matrix", "year": 1999},
    {"title": "Inception", "year": 2010},
    {"title": "Gladiator", "year": 2000},
    {"title": "Interstellar", "year": 2014},
    {"title": "Jurassic Park", "year": 1993}
]

# Function that checks the movie release year
def check_movie(movie):
    if movie["year"] < 2000:
        print("This movie was released before 2000")
        return None
    else:
        print("This movie was released after 2000")
        return movie["title"]

# Empty list
recent_movies = []

# Loop
for movie in favorite_movies:
    result = check_movie(movie)
    if result is not None:
        recent_movies.append(result)

# Final List
print("\nMovies released after 2000:")
print(recent_movies)