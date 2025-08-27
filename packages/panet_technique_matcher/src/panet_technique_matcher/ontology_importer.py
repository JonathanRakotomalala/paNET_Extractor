import owlready2
from owlready2 import base
from .superclass_extractor import extract_subclass_of
import logging

logger = logging.getLogger(__name__)


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
    def fetch_ontology():
        """import the ontology from local or from internet return error if invalid link or path

        Returns:
            an ontology (A generator)

        Raises:
            EmptyOntologyError: if the pathfile/url is wrong or failed to get the ontology
        """
        url = "https://data.bioontology.org/ontologies/PANET/submissions/26/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb"
        try:
            ontology = owlready2.get_ontology(url)
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
                            "subClassOf": extract_subclass_of(i),
                            "definition1": " ".join(i.IAO_0000115),
                            "definition2": "".join(i.IAO_0000119),
                        }
                    )
                return myontology
            else:
                raise EmptyOntologyError()
        except (FileNotFoundError, base.OwlReadyOntologyParsingError) as e:
            logger.error(e)
            if isinstance(e, FileNotFoundError):
                raise OntologyNotFoundError(f"Error cannot find path : {url}")
            else:
                raise EmptyOntologyError(
                    "Error while trying to load ontology : parsing error"
                )
