from recommend import load_movies
from json import load
from sys import argv

if __name__ == '__main__':
    if len(argv) != 3:
        print('Wrong number of parameters.')
    query = argv[1].lower()
    movies_path = argv[2]

    movies = load_movies(movies_path)
    if movies is None:
        exit('File\'s not found.')
    res = [value for key, value in movies.items() if query in key.lower()]
    
    message = 'Results:' if len(res) != 0 else 'Nothing was found.'
    print(message)
    for movie in res:
        print(movie['title'])
