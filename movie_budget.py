import urllib.request
import urllib.parse
import json
from sys import argv
from sys import exit


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


if __name__ == '__main__':
    if len(argv) != 3:
        exit('Неверное количество аргументов.')
    movie_id = int(argv[1])
    api_key = argv[2]
    movie = make_tmdb_api_request('/movie/' + str(movie_id), api_key)

    message = 'Бюджет фильма \"' + movie['title'] +\
              '\" составляет ' + str(movie['budget']) + ' долларов.'
    print(message)
