from .ontology_importer import Ontology
import rapidfuzz
from .score import Score

MAXIMUM_INTEGER = 2147483647


class MatchMapper:
    """
    Makes the matching and the mapping of techniques using normalizing distance function from rapidfuzz
    """

    def my_matcher(input: str, terms, n=10):
        """matches the input to a term inside the list of terms

        Args :
            input: a string
            terms: a list of terms
            n: number of matches (default to 10)
        Returns :
            the term that have the highest proximity or None

        """
        my_func = (
            rapidfuzz.distance.Levenshtein.normalized_distance
        )  # the rapidfuzz distance function to use for the matching

        minimum = MAXIMUM_INTEGER
        distance_found = minimum
        output = {"technique": None, "score": None}
        is_upper_case = input.isupper()
        list_of_technics = []
        nearest_technics = None
        n_first = None

        # the algorithm below only works for distance between terms
        if len(input) > 0:
            for term in terms:
                label_exist = term["label"] != ""
                alt_label_exist = len(term["altLabel"]) > 0
                # if input is an acronym just check altlabels
                if is_upper_case and alt_label_exist:
                    list_of_distances = list(
                        Score.get_altlabels_normalized_distances(
                            input, term["altLabel"], my_func
                        )
                    )
                    distance_found = min(list_of_distances)
                # if not an acronym and no alt label check the label
                elif not (is_upper_case) and label_exist and not (alt_label_exist):
                    distance_found = Score.get_normalized_distance(
                        input, term["label"], my_func
                    )
                # if not an cronym and alt label check label and alt label
                elif not (is_upper_case) and label_exist and alt_label_exist:
                    distance_found_a = Score.get_normalized_distance(
                        input, term["label"], my_func
                    )
                    distances_found_b = list(
                        Score.get_altlabels_normalized_distances(
                            input, term["altLabel"], my_func
                        )
                    )
                    distances_found_b.append(distance_found_a)
                    distance_found = min(distances_found_b)

                match distance_found < 1.0:
                    case True:
                        # list all the technics
                        list_of_technics.append(
                            {"technique": term, "score": distance_found}
                        )

                        if distance_found < minimum:
                            minimum = distance_found
                            output["score"] = distance_found
                            output["technique"] = term

                    case _:
                        continue

        if list_of_technics != []:
            all_technics = sorted(list_of_technics, key=lambda x: x["score"])

            nearest_technics = all_technics[slice(n)]
            n_first = {"n_first": nearest_technics}

        return n_first

    def map_to_panet(my_json, n=1):
        """
        Map the techniques to the paNET ontology
        Args :
            my_json: a json
            n:number of matches to show (default 1)
        Returns :
            a list of the technics in the json and it nearest terms in paNET
        """
        my_ontology = Ontology.getting_ontology()
        my_list = []

        for i in my_json["techniques"]:
            results = MatchMapper.my_matcher(i, my_ontology)["n_first"]
            if results is not None:
                if n != 1:
                    my_list.append({"inText": i, "inPaNET": results.slice(n)})
                else:
                    my_list.append({"inText": i, "inPaNET": results[0]})
        return my_list
