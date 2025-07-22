from ..levenshtein import get_label_distance
from ..levenshtein import get_altlabels_distances
from ..ontology.ontology_import import Ontology

MAXIMUM_INTEGER = 2147483647


class MatchMapper:
    def my_matcher(input: str, terms):
        """ " match the input to a term inside the list of terms

        Args :
            input: a string
            terms: a list of term

        Returns :
            the term that have the highest proximity or None

        """
        minimum = MAXIMUM_INTEGER
        levenshtein_distance_found = minimum
        output = {"technique": None, "score": None}
        is_upper_case = input.isupper()
        list_of_technics = []
        nearest_technics = None
        if len(input) > 0:
            for term in terms:
                label_exist = term["label"] != ""
                alt_label_exist = len(term["altLabel"]) > 0
                # if input is an acronym just check altlabels
                if is_upper_case and alt_label_exist:
                    list_of_distances = list(
                        get_altlabels_distances(input, term["altLabel"])
                    )
                    levenshtein_distance_found = min(list_of_distances)
                # if not an acronym and no alt label check the label
                elif not (is_upper_case) and label_exist and not (alt_label_exist):
                    levenshtein_distance_found = get_label_distance(
                        input, term["label"]
                    )
                # if not an cronym and alt label check label and alt label
                elif not (is_upper_case) and label_exist and alt_label_exist:
                    levenshtein_distance_found_a = get_label_distance(
                        input, term["label"]
                    )
                    levenshtein_distances_found_b = list(
                        get_altlabels_distances(input, term["altLabel"])
                    )
                    levenshtein_distances_found_b.append(levenshtein_distance_found_a)
                    levenshtein_distance_found = min(levenshtein_distances_found_b)

                match levenshtein_distance_found < 1.0:
                    case True:
                        # list all the technics
                        list_of_technics.append(
                            {"technique": term, "score": levenshtein_distance_found}
                        )

                        if levenshtein_distance_found < minimum:
                            minimum = levenshtein_distance_found
                            output["score"] = levenshtein_distance_found
                            output["technique"] = term

                    case _:
                        continue

        if list_of_technics != []:
            all_technics = sorted(list_of_technics, key=lambda x: x["score"])

            nearest_technics = all_technics[slice(10)]

        return {"ten first": nearest_technics}

    def map_to_panet(my_json):
        """
            Map the techniques to the paNET ontology
            Args : 
                my_json a json 
            Returns :
                a list of the technics in the json and it nearest terms in paNET
        """
        my_ontology = Ontology.getting_ontology()
        my_list = []

        for i in my_json["techniques"]:
            results = MatchMapper.my_matcher(i, my_ontology)["ten first"]
            if results is not None:
                print(i, end=": ")
                print(results[0])
                my_list.append({"inText": i, "inPaNET": results[0]})
                print(
                    "________________________________________________________________________\n"
                )
        return my_list

