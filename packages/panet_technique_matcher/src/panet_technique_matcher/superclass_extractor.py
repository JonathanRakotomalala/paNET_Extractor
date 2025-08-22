def extract_subclass_of(a_class):
    """extract the name and label of the classes from which a_class inherits

    Args :
        a_class: an ontology class

    Returns :
        dictionnary containing the classes from which a_class inherit

    """

    # is_a gives the superclass of a_class
    superclass = a_class.is_a
    output = {}
    for i in superclass:
        output[i.name] = " ".join(i.label)
    return output
