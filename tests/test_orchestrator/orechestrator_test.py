from src.orchestrator.orchestrator import Orchestrator
from src.llm import Llm
from src.matchmapper import MatchMapper
from src.ontology import EmptyOntologyError
from src.openaire import OpenAire
import pytest
from fastapi import HTTPException


def test_orchestrator_search_from_text_success(mocker):
    mocker.patch("src.llm.Llm.llm_run",return_value = "{\"techniques\": [\"small-angle scattering\"]}")
    mocker.patch("src.matchmapper.MatchMapper.map_to_panet",return_value =  [{"inText":"Small angle scattering","inPaNET":{"techniques": ["small-angle scattering"]}}])
    result = Orchestrator.search("fffff")

    Llm.llm_run.assert_called_once_with("fffff")
    MatchMapper.map_to_panet.assert_called_once_with({"techniques": ["small-angle scattering"]})

    assert result == {"output":[{"inPaNET":{"techniques": ["small-angle scattering"]},"inText":"Small angle scattering"}]}


def test_orchestrator_list_search_from_dois_success(mocker):
    Orchestrator.time_start=None

    class MockResponse:
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data
    mocker.patch("src.openaire.OpenAire.get_abstract_from_doi", return_value=MockResponse({
        "header": {
            "numFound": 1,
            "maxScore": 1.0,
            "page": 1,
            "pageSize": 10
        },
        "results": [{
            "authors": [{"fullName": "John Doe", "name": None, "surname": None, "rank": 1, "pid": None}],
            "mainTitle": "Some publication",
            "subTitle": None,
            "descriptions": ["fffff"]
        }]
    }))
    mocker.patch("src.orchestrator.Orchestrator.search",return_value = {"output":[{"inPaNET":{"techniques": ["small-angle scattering"]},"inText":"Small angle scattering"}]})

    result = Orchestrator.list_search([("dois",["12345"])])

    Orchestrator.search.assert_called_with("fffff")
    OpenAire.get_abstract_from_doi.assert_called_with("12345")

    assert result == {"outputs":[{"doi":"12345","abstract":"fffff","techniques":{"output":[{"inPaNET":{"techniques": ["small-angle scattering"]},"inText":"Small angle scattering"}]}}]}


def test_orchestrator_search_EmptyOntologyError(mocker):
    mocker.patch("src.llm.Llm.llm_run",return_value = "\"techniques\": [\"small-angle scattering\"]")
    mocker.patch("src.matchmapper.MatchMapper.map_to_panet",side_effect =EmptyOntologyError)

    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")

def test_orchestrator_search_JSONDecoderError(mocker):
    mocker.patch("src.llm.Llm.llm_run",return_value = "\"techniques\": [\"small-angle scattering\"]")

    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")