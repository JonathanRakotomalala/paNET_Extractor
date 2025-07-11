from rapidfuzz.distance import Levenshtein


def get_label_distance(input, my_label):
    """Use rapidfuzz to calculate levenshtein's distance of a label and an input
       Args : 
            input: a string
            label: a string
       Returns : 
            Levenshtein distance of the input and the label

    """
    return round(Levenshtein.normalized_distance(input, my_label), 4)


def get_altlabels_distances(input, my_list):
    """Use rapidfuzz to calculate levenshtein's distance of an alternative labels and an input
       Args :
            input: a string
            my_list a list of string
        Returns :
            a list of integer, each integer is the levenshtein distance of the input and one string of the list
    """
    distances = []
    for i in my_list:
        distances.append(round(Levenshtein.normalized_distance(input, i), 4))
    return distances
