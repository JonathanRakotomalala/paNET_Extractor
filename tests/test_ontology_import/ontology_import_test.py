from packages.panet_technique_matcher.src.panet_technique_matcher.ontology_importer import (
    Ontology,
    EmptyOntologyError,
    OntologyNotFoundError,
)
import pytest
from owlready2 import base


def test_load_ontology(mocker):
    mock_get_ontology = mocker.patch("owlready2.get_ontology")
    # mock of ontology and get_ontology
    mock_ontology = mocker.Mock()
    mock_get_ontology.return_value = mock_ontology
    mock_ontology.load.return_value = mock_ontology

    # mock of classes
    mock_class = mocker.Mock()
    mock_class.label = "mon_label"
    mock_class.IAO_0000115 = "une classe"
    mock_class.IAO_0000119 = "une classe"

    mock_class_1 = mocker.Mock()
    mock_class_1.name = "PaNET1"
    mock_class_1.label = "mon_label_1"

    mock_class_2 = mocker.Mock()
    mock_class_2.name = "PaNET2"
    mock_class_2.label = "mon_label_2"

    mock_class.is_a = [mock_class_1, mock_class_2]

    mock_ontology.classes.return_value = [mock_class]

    url_link = "https://data.bioontology.org/ontologies/PANET/submissions/26/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb"
    results = Ontology.fetch_ontology()

    mock_get_ontology.assert_called_once_with(url_link)
    mock_ontology.load.assert_called_once()
    mock_ontology.classes.assert_any_call()

    assert len(results) > 0


def test_ontology_empty(mocker):
    mock = mocker.Mock()
    mock.load.return_value = []
    mock.classes.return_value = []
    mocker.patch("owlready2.get_ontology", return_value=mock)

    with pytest.raises(EmptyOntologyError):
        Ontology.fetch_ontology()


def test_fail_path_is_invalid(mocker):
    mocker.patch("owlready2.get_ontology", side_effect=FileNotFoundError)

    with pytest.raises(OntologyNotFoundError):
        Ontology.fetch_ontology()


def test_failed_to_load_ontology(mocker):
    mock = mocker.Mock()
    mock.load.side_effect = base.OwlReadyOntologyParsingError
    mocker.patch("owlready2.get_ontology", return_value=mock)

    with pytest.raises(EmptyOntologyError):
        Ontology.fetch_ontology()
