from json import load
from sys import argv

if __name__ == '__main__':
    if len(argv) != 3:
        print('Неверное количество аргументов.')
    query = argv[1].lower()
    database_path = argv[2]

    movies = None
    with open(database_path, 'r') as f:
        movies = load(f)
    res = [value for key, value in movies.items() if query in key.lower()]
    
    print('Результаты:')
    for movie in res:
        print(movie['title'])
