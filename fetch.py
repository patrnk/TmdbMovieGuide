from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.parse import urlencode
from json import dump
from json import loads
from argparse import ArgumentParser
from getpass import getpass
from os.path import exists
from distutils.util import strtobool
from sys import exit


def load_json_data_from_url(base_url, url_params):
    url = '%s?%s' % (base_url, urlencode(url_params))
    response = urlopen(url).read().decode('utf-8')
    return loads(response)


def make_tmdb_api_request(method, api_key, extra_params=None):
    extra_params = extra_params or {}
    url = 'https://api.themoviedb.org/3%s' % method
    params = {
        'api_key': api_key,
        'language': 'en',
    }
    params.update(extra_params)
    too_many_requests = 429
    cooldown_time_in_seconds = 10
    try:
        json_data = load_json_data_from_url(url, params)
    except HTTPError as error:
        if error.code == too_many_requests:
            sleep(cooldown_time_in_seconds)
            json_data = load_json_data_from_url(url, params)
        else:
            raise
    return json_data


def get_movie_ids_from_tmdb(number_of_ids, api_key):
    request_params = {'page': 1, 'include_adult': True}
    movie_ids = []
    movies_per_page = 20
    for i in range(0, number_of_ids, movies_per_page):
        response_page = make_tmdb_api_request('/discover/movie',\
                                              api_key, request_params)
        for movie in response_page['results']:
            movie_ids.append(movie['id'])
            if len(movie_ids) >= number_of_ids:
                break
        request_params['page'] += 1
    return movie_ids


def get_movie_info_from_tmdb(movie_id, api_key):
    movie_info = {}
    details_query = '/movie/%d' % movie_id
    keywords_query =  '%s/keywords' % details_query
    
    details = make_tmdb_api_request(details_query, api_key)
    keywords = make_tmdb_api_request(keywords_query, api_key)
    
    movie_info = details
    movie_info.update(keywords)
    return movie_info


def get_movies_info_from_tmdb(movie_ids, api_key):
    movies_info = {}
    for movie_id in movie_ids:
        movie_info = get_movie_info_from_tmdb(movie_id, api_key)
        movies_info[movie_info['title']] = movie_info
    

def show_delete_prompt(query):
    while True:
        val = input('%s [y/n]: ' % query)
        try:
            answer = strtobool(val)
        except ValueError:
            print('Please answer with either yes or no')
            continue
        return answer


def get_args():
    parser = ArgumentParser()
    parser.add_argument('movies_to_download', type=int,
                        help='number of movies to download')
    parser.add_argument('-o', '--outfile', type=str, default='movies.json',
                        help='output file, in JSON format')
    args = parser.parse_args()
    return args
    

def prompt_if_exists(outfile):
    if exists(outfile):
        query = '%s already exists. Rewrite?' % args.outfile
        if not show_delete_prompt(query):
            print('Nothing was written.')
            exit(0)


if __name__ == '__main__':
    args = get_args()
    api_key = getpass('TMDB API key:')
    prompt_if_exists(args.outfile)

    print('Downloading ids...')
    try:
        movie_ids = get_movie_ids_from_tmdb(args.movies_to_download, 
                                       api_key)
    except HTTPError as error:
        exit('Error %d.' % error.code)

    print('Getting additional info...')
    try:
        movies_info = get_movies_info_from_tmdb(movie_ids, api_key)
    except HTTPError as error:
        exit('Error %d.' % error.code)
    
    print('Writing to a json-file...')
    with open(args.outfile, 'w') as f:
        dump(movies_info, f)
    print('Done!')
