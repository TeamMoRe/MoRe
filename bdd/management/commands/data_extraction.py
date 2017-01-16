import io
import os
import sys
from zipfile import ZipFile
from django.core.management.base import BaseCommand

import datetime
import urllib.request
import shutil


DATA_URL = 'http://files.grouplens.org/datasets/movielens/ml-100k.zip'
DATA_FILE_NAME = os.path.join(os.path.dirname(__file__), "resources/ml-100k.zip").replace("\\", "/")
#BASE_DIRECTORY = os.path.splitext(os.path.basename(DATA_FILE_NAME))[0]
BASE_DIRECTORY=os.path.join(os.path.dirname(__file__), "resources/ml-100k/").replace("\\", "/")

def get_data():
    download_file_if_not_present(DATA_FILE_NAME, DATA_URL)
    users = {user.id: user for user in get_users()}
    movies = {movie.id: movie for movie in get_movies()}
    ratings = get_ratings()

    return users, movies, ratings


def split_ratings_by_users_and_by_movies(ratings):
    ratings_by_users = {}
    ratingsy_movies = {}

    for rating in ratings:
        if rating.user_id not in ratings_by_users:
            ratings_by_users[rating.user_id] = []
        if rating.movie_id not in ratings_by_movies:
            ratings_by_movies[rating.movie_id] = []

        ratings_by_users[rating.user_id].append(rating)
        ratings_by_movies[rating.movie_id].append(rating)

    return ratings_by_users, ratings_by_movies


def download_file_if_not_present(file_name, url):
    if not os.path.isfile(file_name):
        print("download file from:", url, datetime.datetime.now(), file=sys.stderr)
        print("save it in:", file_name, file=sys.stderr)

        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        print("data saved.", file=sys.stderr)


def get_users():
    return get_data_file("u.user", User.from_file_line)


def get_movies():
    return get_data_file("u.item", Movie.from_file_line)


def get_ratings():
    return get_data_file("u.data", Rating.from_file_line)


def get_data_file(file_name, method_for_extract_a_line):
    #with ZipFile(DATA_FILE_NAME) as myzip:
    #   file = io.TextIOWrapper(myzip.open(os.path.join(BASE_DIRECTORY, file_name)), errors='ignore')
    #    data_structure = [method_for_extract_a_line(line.strip()) for line in file]
    with open(os.path.join(BASE_DIRECTORY,file_name), 'r') as file:
        data_structure=[method_for_extract_a_line(line.strip()) for line in file]
    return data_structure


class Movie:
    @classmethod
    def from_file_line(cls, line, separator="|"):
        line_split = line.split(separator)
        id_movie, title, release_date, video_release_date, imdb_url = line_split[:5]

        return cls(int(id_movie),
                   title,
                   release_date,
                   video_release_date,
                   imdb_url, [Genre(int(i)) for i, x in enumerate(line_split[6:]) if x == "1"])

    def __init__(self, id_movie, title, release_date, video_release_date, imdb_url, genres):
        self.id = id_movie
        self.title = title
        self.release_date = release_date
        self.video_release_date = video_release_date
        self.imdb_url = imdb_url
        self.genres = list(genres)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Movie(" + ", ".join([str(self.id),
                                     str(self.title),
                                     self.release_date,
                                     self.video_release_date,
                                     self.imdb_url]) + ", " + \
               str(self.genres) + ")"


class Genre:
    TYPE = ["unknown",
            "action",
            "adventure",
            "animation",
            "children",
            "comedy",
            "crime",
            "documentary",
            "drama",
            "fantasy",
            "film_noir",
            "horror",
            "musical",
            "mystery",
            "romance",
            "sci_fi",
            "thriller",
            "war",
            "western"]

    def __init__(self, genre_type):
        self._type = genre_type

    def __repr__(self):
        return Genre.TYPE[self._type]

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        """
        :type other: Genre
        """
        return self._type == other._type


class User:
    @classmethod
    def from_file_line(cls, line, separator="|"):
        id_user, age, gender, occupation, zip_code = line.split(separator)
        return cls(int(id_user),
                   int(age),
                   gender,
                   occupation,
                   zip_code)

    def __init__(self, id_user, age, gender, occupation, zip_code):
        self.id = id_user
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.zip_code = zip_code

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "User(" + ", ".join([str(self.id),
                                    str(self.age),
                                    self.gender,
                                    self.occupation,
                                    self.zip_code]) + ")"


class Rating:
    @classmethod
    def from_file_line(cls, line, separator=""):
        user_id, movie_id, note, timestamp = separator and line.split(separator) or line.split()
        return cls(int(user_id),
                   int(movie_id),
                   int(note),
                   timestamp)

    def __init__(self, user_id, movie_id, note, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.note = note
        self.timestamp = timestamp

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "Rating(" + ", ".join(["user_id=" + str(self.user_id),
                                      "movie_id=" + str(self.movie_id),
                                      str(self.note),
                                      str(self.timestamp)]) + ")"




