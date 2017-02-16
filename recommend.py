from os.path import exists
from argparse import ArgumentParser
from json import load
from sys import argv
from sys import exit


def count_common_items_in_lists(list1, list2):
    return len(set(list1) & set(list2))


def is_almost_equal_to(num1, num2, difference_range):
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

    collection1 = movie1['belongs_to_collection'] 
    collection2 = movie2['belongs_to_collection']
    if collection1 is not None and collection2 is not None:
        if collection1['id'] == collection2['id']:
            rating += weight['belongs_to_collection']

    strict_criteria = ['keywords', 'genres', 'production_companies']
    for criterion in strict_criteria:
        if movie1[criterion] is None or movie2[criterion] is None:
            continue
        items1 = [item['id'] for item in movie1[criterion]]
        items2 = [item['id'] for item in movie2[criterion]] 
        common_items = count_common_items_in_lists(items1, items2)
        rating += common_items * weight[criterion]

    loose_criteria = ['budget', 'runtime', 'vote_average']
    accuracy = {'budget': 0.2, 'runtime': 0.15, 'vote_average': 0.2}
    for criterion in loose_criteria:
        if movie1[criterion] is None or movie2[criterion] is None:
            continue
        is_equal = is_almost_equal_to(movie1[criterion], movie2[criterion],
                                   movie2[criterion] * accuracy[criterion])
        rating += int(is_equal) * weight[criterion]
        
    return rating


def load_movies_from_file(filepath):
    if not exists(filepath):
        return None
    with open(filepath, 'r') as f:
        return load(f)


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('query', help='the exact name of the movie ' + 
                        'upon which the recommendations are based')
    parser.add_argument('-t', '--top', type=int, default=5, 
                        help='the number of recommendations to make')
    parser.add_argument('-i', '--infile', type=str, default='movies.json', 
                        help='input file, in JSON format')
    return parser


def get_top_recommended_movies(database, top_count):
    chart = [(get_similarity_rating(movie, target), title) 
             for title, movie in database.items()]
    chart.sort(reverse = True)
    return [title for _, title in chart[:top_count]]
    

if __name__ == '__main__':
    args = get_argument_parser().parse_args()

    database = load_movies_from_file(args.infile)
    if database is None:
        exit('File\'s not found.')

    if args.query not in database:
        exit('File doesn\'t contain any info about the movie.')
    target = database.pop(args.query)

    print('Recommendations:')
    print('\n'.join(get_top_recommended_movies(database, args.top)))
