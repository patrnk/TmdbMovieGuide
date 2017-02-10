from download_db import make_tmdb_api_request
from sys import argv
from sys import exit

if __name__ == '__main__':
    if len(argv) != 3:
        exit('Неверное количество аргументов.')
    movie_id = int(argv[1])
    api_key = argv[2]
    movie = make_tmdb_api_request('/movie/' + str(movie_id), api_key)

    message = 'Бюджет фильма \"' + movie['title'] +\
              '\" составляет ' + str(movie['budget']) + ' долларов.'
    print(message)
