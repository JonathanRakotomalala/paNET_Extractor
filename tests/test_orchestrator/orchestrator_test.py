from src.orchestrator.orchestrator import Orchestrator
from src.llm import Llm
from src.matchmapper import MatchMapper
from src.ontology import EmptyOntologyError
from src.openaire import OpenAire, RateLimitError
import pytest
from fastapi import HTTPException
import time

def test_orchestrator_search_from_text_success(mocker):
    mocker.patch("src.llm.Llm.llm_run",return_value = "{\"techniques\": [\"small-angle scattering\"]}")
    mocker.patch("src.matchmapper.MatchMapper.map_to_panet",return_value =  [{"inText":"small-angle scattering","inPaNET":{"technique": {"small-angle scattering"}},"score":0.0}])
    result = Orchestrator.search("fffff")

    Llm.llm_run.assert_called_once_with("fffff")
    MatchMapper.map_to_panet.assert_called_once_with({"techniques": ["small-angle scattering"]})

    assert result == {"algorithm":"Levenshtein's distance","output":[{"inPaNET":{"technique": {"small-angle scattering"}},"inText":"small-angle scattering","score":0.0}]}


def test_orchestrator_list_search_from_dois_success(mocker):
    Orchestrator.time_start=None
    mocker.patch("src.openaire.OpenAire.get_abstract_from_doi", return_value="fffff")
    mocker.patch("src.orchestrator.Orchestrator.search",return_value = {"algorithm":"Levenshtein's distance","output":[{"inPaNET":{"technique": {"small-angle scattering"}},"inText":"small-angle scattering","score":0.0}]})

    result = Orchestrator.list_search([("dois",["12345"])])

    Orchestrator.search.assert_called_with("fffff")
    OpenAire.get_abstract_from_doi.assert_called_with("12345")

    assert result == {"algorithm":"Levenshtein's distance","outputs":[{"doi":"12345","abstract":"fffff","techniques":[{"inPaNET":{"technique": {"small-angle scattering"}},"inText":"small-angle scattering","score":0.0}]}]}

def test_orchestrator_list_search_no_abstract(mocker):
    mocker.patch("src.openaire.OpenAire.get_abstract_from_doi",return_value = "No abstract available")

    result = Orchestrator.list_search([('doi',['12345'])])
    
    assert result == {"algorithm":"Levenshtein's distance",'outputs':[{"doi": '12345', "abstract": "No abstract available", "techniques": []}]}

def test_orchestrator_search_EmptyOntologyError(mocker):
    mocker.patch("src.llm.Llm.llm_run",return_value = "\"techniques\": [\"small-angle scattering\"]")
    mocker.patch("src.matchmapper.MatchMapper.map_to_panet",side_effect =EmptyOntologyError)

    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")

def test_orchestrator_search_JSONDecoderError(mocker):
    mocker.patch("src.llm.Llm.llm_run",return_value = "\"techniques\": [\"small-angle scattering\"]")

    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")

def test_orchestrator_search_ontology_not_found(mocker):
    mocker.patch("src.ontology.ontology_import.Ontology.getting_ontology",side_effect = EmptyOntologyError)
    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")

def test_orchestrator_list_search_no_techniques_when_search_raises_exceptions(mocker):
    mocker.patch("src.orchestrator.orchestrator.Orchestrator.search",side_effect = HTTPException(
                    status_code=400,
                    detail="Bad Request",
                    headers={"message": "Bad Request"},
                ))
    result =    Orchestrator.list_search([("doi",["12345"])])

    assert result['outputs'][0]['techniques']== []




def test_orchestrator_list_search_RateLimitError_raises_http_exception(mocker):
    mocker.patch("src.openaire.OpenAire.get_abstract_from_doi",side_effect = RateLimitError(time.time()+10))

    with pytest.raises(HTTPException):
        Orchestrator.list_search([("doi",["12345"])])

def test_orchestrator_list_search_RateLimitError_raises_ratelimit_then_http_exception(mocker):
    Orchestrator.time_start = time.time() +60
    with pytest.raises(HTTPException):
        Orchestrator.list_search([("doi",["12345"])])