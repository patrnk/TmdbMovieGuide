from download_db import get_movie_info_from_tmdb
from urllib.error import HTTPError
from sys import argv
from sys import exit

if __name__ == '__main__':
    if len(argv) != 3:
        exit('Неверное количество аргументов.')
    movie_id = int(argv[1])
    api_key = argv[2]

    try:
        movie = get_movie_info_from_tmdb(movie_id, api_key)
    except HTTPError as error:
        if error.code == 401:
            exit('Неверный API ключ.')
        else:
            exit('Ошибка %s.' % error.code)

    message = 'Бюджет фильма \"%s\" составляет %d долларов.'
    message = message % (movie['title'], movie['budget'])
    print(message)
