def get_normalized_distance(input:str,term:str,fun):
    return fun(input,term)


def get_altlabels_normalized_distances(input, my_list,fun):
    """Use rapidfuzz to calculate levenshtein's distance of an alternative labels and an input
       Args :
            input: a string
            my_list a list of string
        Returns :
            a list of integer, each integer is the levenshtein distance of the input and one string of the list
    """
    distances = []
    for i in my_list:
        distances.append(round(fun(input, i), 4))
    return distances
