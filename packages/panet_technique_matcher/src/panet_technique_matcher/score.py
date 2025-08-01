class Score:
    def get_normalized_distance(input: str, term: str, fun):
        """gets the normalized distance between two words
        Args:
            input: A string
            term: A string
            fun: A function that takes two strings as parameters and returns a float
        Returns:
            A float that represents the distance between two strings
        """
        return round(fun(input, term), 4)

    def get_altlabels_normalized_distances(input, my_list, fun):
        """gets distance of an alternative labels and an input
        Args :
            input: A string
            my_list: A list of string
            fun: A function that takes two strings as parameters
        Returns :
            a list of float, each float is the levenshtein distance of the input and one string of the list
        """
        distances = []
        for i in my_list:
            distances.append(round(fun(input, i), 4))
        return distances
