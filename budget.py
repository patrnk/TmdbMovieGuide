from fetch import get_movie_info_from_tmdb
from urllib.error import HTTPError
from getpass import getpass
from sys import exit
import argparse


def get_movie_id_and_api_key():
    parser = argparse.ArgumentParser()
    parser.add_argument('movie_id', 
                        help='id of the movie to get info about', type=int)
    args = parser.parse_args()
    api_key = getpass('TMDB API key:')
    return (args.movie_id, api_key)


def get_movie(movie_id, api_key):
    try:
        movie = get_movie_info_from_tmdb(movie_id, api_key)
    except HTTPError as error:
        if error.code == 401:
            exit('Bad API key.')
        else:
            exit('Error %s.' % error.code)
    return movie


def print_movie_budget(movie):
    message = 'The budget of the movie \"%s\" is %s.'
    budget = "$%d" % movie['budget'] if movie['budget'] != 0 else 'unknown'
    message = message % (movie['title'], budget)
    print(message)


if __name__ == '__main__':
    movie_id, api_key = get_movie_id_and_api_key()
    movie = get_movie(movie_id, api_key)
    print_movie_budget(movie)
