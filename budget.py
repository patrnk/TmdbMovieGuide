from fetch import get_movie_info_from_tmdb
from fetch import is_tmdb_available
from fetch import is_valid_tmdb_api_v3_key
from getpass import getpass
from sys import exit
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()
    parser.add_argument('movie_id', 
                        help='id of the movie to get info about', type=int)
    args = parser.parse_args()
    return args


def get_movie(movie_id, api_key):
    movie = get_movie_info_from_tmdb(movie_id, api_key)
    return movie


def print_movie_budget(movie):
    message = 'The budget of the movie \"%s\" is %s.'
    budget = "$%d" % movie['budget'] if movie['budget'] != 0 else 'unknown'
    message = message % (movie['title'], budget)
    print(message)


if __name__ == '__main__':
    args = get_args()
    api_key = getpass('TMDB API key: ')

    if not is_tmdb_available():
        exit('Can\'t connect to TMDB')
    if not is_valid_tmdb_api_v3_key(api_key):
        exit('Bad API key.')

    movie = get_movie(args.movie_id, api_key)
    print_movie_budget(movie)
