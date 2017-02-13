from os.path import exists
from json import load
from sys import argv
from sys import exit


def count_common_items_in_lists(list1, list2):
    return len(set(list1) & set(list2))


def numbers_differ_in_range(num1, num2, difference_range):
    if lhs or rhs is None:
        return False
    return num1 - difference_range <= num2 <= num1 + difference_range


def get_similarity_rating(movie1, movie2):
    '''Returns an integer indicating how similar the two movies.
        
    Minimum possible rating is 0. 
    Maximum possible rating is determined by get_similarity_rating(a, a).
    Note that get_similarity_rating(a, b) is not necessarily 
    equal to get_similarity_rating(b, a).
    '''
    weight = {'belongs_to_collection': 1000, 'keywords': 200, 'genres': 100,
              'production_companies': 150, 'budget': 30, 'runtime': 40, 
              'vote_average': 30}
    rating = 0

    strict_criteria = ['collection', 'keywords', 
                       'genres', 'production_companies']
    for criterion in strict_criteria:
        items1 = [item['id'] for item in movie1[criterion]]
        items2 = [item['id'] for item in movie2[criterion]]
        common_items = count_common_items_in_lists(items1, items2)
        rating += common_items * weight[criterion]

    loose_criteria = ['budget', 'runtime', 'vote_average']
    accuracy = {'budget': 0.2, 'runtime': 0.15, 'vote_average': 0.2}
    for criterion in loose_criteria:
        is_equal = almost_equal(movie1[criterion], movie2[criterion],
                                movie2[criterion] * accuracy[criterion])
        rating += int(is_equal) * weight[criterion]
        
    return rating


def load_movies_from_file(filepath):
    if not exists(filepath):
        return None
    with open(filepath, 'r') as f:
        return load(f)


if __name__ == '__main__':
    if len(argv) != 4:
        exit('Неверное количество аргументов.')
    query = argv[1]
    top_count = int(argv[2])
    filename = argv[3]

    database = load_movies_from_file(filename)
    if database is None:
        exit('Файл не найден.')

    if query not in database:
        exit('Этого фильма нет в базе.')
    target = database.pop(query)

    chart = [(get_similarity_rating(movie, target), title) 
             for title, movie in database.items()]
    chart.sort(reverse = True)
    
    print('Рекомендуем:')
    for rating, title in chart[:top_count]:
        print(title)
