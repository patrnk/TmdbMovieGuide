import urllib.request
import urllib.parse
import json
from sys import argv
from sys import exit
from json import dump
from json import load


def load_json_data_fron_url(base_url, url_params):
    url = '%s?%s' % (base_url, urllib.parse.urlencode(url_params))
    response = urllib.request.urlopen(url).read().decode('utf-8')
    return json.loads(response)


def make_tmdb_api_request(method, api_key, extra_params=None):
    extra_params = extra_params or {}
    url = 'https://api.themoviedb.org/3%s' % method
    params = {
        'api_key': api_key,
        'language': 'ru',
    }
    params.update(extra_params)
    return load_json_data_fron_url(url, params)


def get_movie_ids_from_tmdb(number_of_ids):
    request_params = {'page': 1, 'include_adult': True}
    movie_ids = []
    while len(movie_ids) < number_of_ids:
        response_page = make_tmdb_api_request('/discover/movie',\
                                              api_key, request_params)
        for movie in response_page['results']:
            movie_ids.append(movie['id'])
            if len(movie_ids) >= number_of_ids:
                break
        request_params['page'] += 1
    return movie_ids


def get_movie_info_from_tmdb(movie_id):
    movie_info = {}
    details_query = '/movie/' + str(movie_id)
    keywords_query = details_query + '/keywords'
    
    details = make_tmdb_api_request(details_query, api_key)
    keywords = make_tmdb_api_request(keywords_query, api_key)
    
    movie_info = details
    movie_info.update(keywords)
    return movie_info


if __name__ == '__main__':
    if len(argv) != 4:
        print('Неверное количество аргументов.')
    movies_to_download = int(argv[1])
    file_to_save = argv[2]
    api_key = argv[3]

    print('Скачиваем идентификаторы...')
    movie_ids = get_movie_ids_from_tmdb(movies_to_download)

    print('Узнаем подробности...')
    movies_info = {}
    for movie_id in movie_ids:
        movie_info = get_movie_info_from_tmdb(movie_id)
        movies_info[movie_info['title']] = movie_info

    print('Записываем в json-файл...')
    with open(file_to_save, 'w') as f:
        dump(movies_info, f)
    print('Готово!')
