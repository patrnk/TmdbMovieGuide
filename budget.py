from fetch import get_movie_info_from_tmdb
from urllib.error import HTTPError
from sys import argv
from sys import exit


def get_movie_id_and_api_key(argv):
    if len(argv) != 3:
        exit('Неверное количество аргументов.')
    movie_id = int(argv[1])
    api_key = argv[2]
    return (movie_id, api_key)
    

def get_movie(movie_id, api_key):
    try:
        movie = get_movie_info_from_tmdb(movie_id, api_key)
    except HTTPError as error:
        if error.code == 401:
            exit('Неверный API ключ.')
        else:
            exit('Ошибка %s.' % error.code)
    return movie


def output_movie_budget(movie):
    message = 'Бюджет фильма \"%s\" составляет %d долларов.'
    message = message % (movie['title'], movie['budget'])
    print(message)


if __name__ == '__main__':
    movie_id, api_key = get_movie_id_and_api_key(argv)
    movie = get_movie(movie_id, api_key)
    output_movie_budget(movie)
