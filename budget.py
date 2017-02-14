from fetch import get_movie_info_from_tmdb
from urllib.error import HTTPError
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
    args = get_args()
    api_key = getpass('TMDB API key:')
    movie = get_movie(args.movie_id, api_key)
    print_movie_budget(movie)
