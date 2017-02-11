from json import load
from sys import argv
from sys import exit


def count_common_elements(lhs, rhs, key):
    lhs_item_set = set([item['id'] for item in lhs[key]])
    rhs_item_set = set([item['id'] for item in rhs[key]])
    return len(lhs_item_set & rhs_item_set) 


def almost_equal(lhs, rhs, error_range):
    if lhs is None or rhs is None:
        return False
    return lhs - error_range <= rhs and rhs <= lhs + error_range


def get_rating(candidate, model):
    weight = {'belongs_to_collection': 1000, 'keywords': 200, 'genres': 100,
              'production_companies': 150, 'budget': 30, 'runtime': 40, 
              'vote_average': 30}
    rating = 0

    candidate_collection = candidate['belongs_to_collection']
    model_collection = model['belongs_to_collection']
    if candidate_collection is not None and model_collection is not None:
        if candidate_collection['id'] == model_collection['id']:
            rating += weight['belongs_to_collection']

    strict_criteria = ['keywords', 'genres', 'production_companies']
    for criterion in strict_criteria:
        common_elements = count_common_elements(candidate, model, criterion)
        rating += common_elements * weight[criterion]

    loose_criteria = ['budget', 'runtime', 'vote_average']
    accuracy = {'budget': 0.2, 'runtime': 0.15, 'vote_average': 0.2}
    for criterion in loose_criteria:
        is_equal = almost_equal(candidate[criterion], model[criterion],
                                model[criterion] * accuracy[criterion])
        rating += int(is_equal) * weight[criterion]
        
    return rating


def load_movies(filename):
    with open(filename, 'r') as f:
        return load(f)


if __name__ == '__main__':
    if len(argv) != 4:
        exit('Неверное количество аргументов.')
    query = argv[1]
    top_count = int(argv[2])
    filename = argv[3]

    database = load_movies(filename)

    if query not in database:
        exit('Этого фильма нет в базе.')
    target = database.pop(query)

    chart = [(get_rating(movie, target), title) 
             for title, movie in database.items()]
    chart.sort(reverse = True)
    
    print('Рекомендуем:')
    for rating, title in chart[:top_count]:
        print(title)
