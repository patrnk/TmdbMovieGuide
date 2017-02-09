from tmdb_api_helpers import make_tmdb_api_request
from sys import argv
from sys import exit

if __name__ == '__main__':
    if len(argv) != 3:
        print('Неверное количество аргументов.')
    movies_to_download = int(argv[1])
    api_key = argv[2]

    print('Скачиваем идентификаторы...')
    request_params = {'page': 1, 'include_adult': True}
    movie_ids = []
    while len(movie_ids) < movies_to_download:
        response_page = make_tmdb_api_request('/discover/movie',\
                                              api_key, request_params)
        for movie in response_page['results']:
            movie_ids.append(movie['id'])
        request_params['page'] += 1

    print('Узнаем подробности...')
    movies_info = {}
    for movie_id in movie_ids:
        details_query = '/movie/' + str(movie_id)
        keywords_query = details_query + '/keywords'
        lists_query = details_query + '/lists'

        details = make_tmdb_api_request(details_query, api_key)
        keywords = make_tmdb_api_request(keywords_query, api_key)
        lists = make_tmdb_api_request(lists_query, api_key)

        movies_info[movie_id] = details
        movies_info[movie_id].update(keywords)
        movies_info[movie_id]['lists'] = lists['results']

