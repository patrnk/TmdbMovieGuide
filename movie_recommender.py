from json import load
from sys import argv


def count_common_elements(lhs, rhs, key):
    lhs_item_set = set([item['id'] for item in lhs[key]])
    rhs_item_set = set([item['id'] for item in rhs[key]])
    return len(lhs_item_set & rhs_item_set) 


def almost_equal(lhs, rhs, error_range):
    return lhs - error_range <= rhs and rhs <= lhs + error_range


def form_similarity_rating(candidate, model):
    weight = {'belongs_to_collection': 1000, 'keywords': 200, 'genres': 100,
              'budget': 30, 'runtime': 40, 'vote_average': 30}
    rating = 0

    candidate_collection = candidate['belongs_to_collection']
    model_collection = model['belongs_to_collection']
    if candidate_collection is not None and model_collection is not None:
        if candidate_collection['id'] == model_collection['id']:
            rating += weight['belongs_to_collection']

    common_keywords = count_common_elements(candidate, model, 'keywords')
    rating += common_keywords * weight['keywords']
    common_genres = count_common_elements(candidate, model, 'genres')
    rating += common_genres * weight['genres']

    light_criteria = ['budget', 'runtime', 'vote_average']
    accuracy = {'budget': 0.2, 'runtime': 0.15, 'vote_average': 0.2}
    for criterion in light_criteria:
        is_equal = almost_equal(candidate[criterion], model[criterion],
                                model[criterion] * accuracy[criterion])
        rating += int(is_equal) * weight[criterion]
        
    return rating


if __name__ == '__main__':
    movies_info = None
    with open('movies.json', 'r') as f:
        movies_info = load(f)
    for title in movies_info.keys():
        print(title)
    lhs = movies_info['История игрушек 2']
    rhs = movies_info['Пингвины Мадагаскара']
    print(form_similarity_rating(lhs, rhs))
