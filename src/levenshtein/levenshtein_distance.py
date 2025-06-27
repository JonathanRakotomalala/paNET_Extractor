from rapidfuzz.distance import Levenshtein


def get_label_distance(input, my_label):
    """Use rapidfuzz to calculate levenshtein's distance of a label and an input"""
    return round(Levenshtein.normalized_distance(input, my_label), 4)


def get_altlabels_distances(input, my_list):
    """Use rapidfuzz to calculate levenshtein's distance of an alternative labels and an input"""
    distances = []
    for i in my_list:
        distances.append(round(Levenshtein.normalized_distance(input, i), 4))
    return distances
