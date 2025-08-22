import owlready2
from owlready2 import base


class EmptyOntologyError(Exception):
    def __init__(self, message="Ontology must not be empty"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class OntologyNotFoundError(Exception):
    def __init__(self, message="Wrong path"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class Ontology:
    def getting_ontology():
        """import the ontology from local or from internet return error if invalid link or path

        Returns:
            an ontology (A generator)

        Raises:
            EmptyOntologyError: if the pathfile/url is wrong or failed to get the ontology
        """

        try:
            ontology = owlready2.get_ontology(
                "https://data.bioontology.org/ontologies/PANET/submissions/26/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb"
            )
            ontology.load()
            classes = ontology.classes()
            # we don't use the classes variable to get the length because the transformation of a generator into a list is definitive
            # and we need to get a new generator (with ontology.classes()) again to iterate on the ontology's classes
            length = len(list(ontology.classes()))
            myontology = []
            if length > 0:
                for i in classes:
                    myontology.append(
                        {
                            "id": i.iri,
                            "label": "".join(i.label),
                            "altLabel": i.altLabel,
                            "subClassOf": Ontology.extract_subclass_of(i),
                            "definition1": " ".join(i.IAO_0000115),
                            "definition2": "".join(i.IAO_0000119),
                        }
                    )
                return myontology
            else:
                raise EmptyOntologyError()
        except (FileNotFoundError, base.OwlReadyOntologyParsingError) as e:
            if isinstance(e, FileNotFoundError):
                raise OntologyNotFoundError("Error cannot find path")
            else:
                raise EmptyOntologyError(
                    "Error while trying to load ontology: ontology not found"
                )

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
