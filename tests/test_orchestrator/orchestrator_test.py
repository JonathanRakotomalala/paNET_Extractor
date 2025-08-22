from src.panetextractor.orchestrator import Orchestrator
from packages.techniques_extractor.src.techniques_extractor import Llm
from packages.panet_technique_matcher.src.panet_technique_matcher import MatchMapper
from packages.panet_technique_matcher.src.panet_technique_matcher.ontology_importer import (
    EmptyOntologyError,
    OntologyNotFoundError,
)
from packages.data_provider.src.data_provider import DataProvider, RateLimitError
import pytest
from fastapi import HTTPException
import time


def test_orchestrator_search_from_text_success(mocker):
    mocker.patch(
        "packages.techniques_extractor.src.techniques_extractor.Llm.llm_run",
        return_value='{"techniques": ["small-angle scattering"]}',
    )
    mocker.patch(
        "packages.panet_technique_matcher.src.panet_technique_matcher.matchmapper.MatchMapper.map_to_panet",
        return_value=[
            {
                "inText": "small-angle scattering",
                "inPaNET": {"technique": {"small-angle scattering"}},
                "score": 0.0,
            }
        ],
    )
    result = Orchestrator.search("fffff")

    Llm.llm_run.assert_called_once_with("fffff")
    MatchMapper.map_to_panet.assert_called_once_with(
        {"techniques": ["small-angle scattering"]}
    )

    assert result == {
        "algorithm": "Levenshtein's distance",
        "output": [
            {
                "inPaNET": {"technique": {"small-angle scattering"}},
                "inText": "small-angle scattering",
                "score": 0.0,
            }
        ],
    }


def test_orchestrator_list_search_from_dois_success(mocker):
    Orchestrator.time_start = None
    mocker.patch(
        "packages.data_provider.src.data_provider.DataProvider.get_abstract_from_doi",
        return_value="fffff",
    )
    mocker.patch(
        "src.panetextractor.orchestrator.Orchestrator.search",
        return_value={
            "algorithm": "Levenshtein's distance",
            "output": [
                {
                    "inPaNET": {"technique": {"small-angle scattering"}},
                    "inText": "small-angle scattering",
                    "score": 0.0,
                }
            ],
        },
    )

    result = Orchestrator.list_search([("dois", ["12345"])])

    Orchestrator.search.assert_called_with("fffff")
    DataProvider.get_abstract_from_doi.assert_called_with("12345")

    assert result == {
        "algorithm": "Levenshtein's distance",
        "outputs": [
            {
                "doi": "12345",
                "abstract": "fffff",
                "techniques": [
                    {
                        "inPaNET": {"technique": {"small-angle scattering"}},
                        "inText": "small-angle scattering",
                        "score": 0.0,
                    }
                ],
            }
        ],
    }


def test_orchestrator_list_search_no_abstract(mocker):
    mocker.patch(
        "packages.data_provider.src.data_provider.DataProvider.get_abstract_from_doi",
        return_value="No abstract available",
    )

    result = Orchestrator.list_search([("doi", ["12345"])])

    assert result == {
        "algorithm": "Levenshtein's distance",
        "outputs": [
            {"doi": "12345", "abstract": "No abstract available", "techniques": []}
        ],
    }


def test_orchestrator_search_EmptyOntologyError(mocker):
    mocker.patch(
        "packages.techniques_extractor.src.techniques_extractor.Llm.llm_run",
        return_value='"techniques": ["small-angle scattering"]',
    )
    mocker.patch(
        "packages.panet_technique_matcher.src.panet_technique_matcher.matchmapper.MatchMapper.map_to_panet",
        side_effect=EmptyOntologyError,
    )

    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")


def test_orchestrator_search_JSONDecoderError(mocker):
    mocker.patch(
        "packages.techniques_extractor.src.techniques_extractor.Llm.llm_run",
        return_value='"techniques": ["small-angle scattering"]',
    )

    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")


def test_orchestrator_search_ontology_not_found(mocker):
    mocker.patch(
        "packages.panet_technique_matcher.src.panet_technique_matcher.ontology_importer.Ontology.getting_ontology",
        side_effect=EmptyOntologyError,
    )
    with pytest.raises(HTTPException):
        Orchestrator.search("fffff")


def test_orchestrator_list_search_no_techniques_when_search_raises_exceptions(mocker):
    mocker.patch(
        "src.panetextractor.orchestrator.orchestrator.Orchestrator.search",
        side_effect=HTTPException(
            status_code=400,
            detail="Bad Request",
            headers={"message": "Bad Request"},
        ),
    )
    result = Orchestrator.list_search([("doi", ["12345"])])

    assert (
        result["outputs"][0]["techniques"]
        == "Error could not extract and map techniques"
    )


def test_orchestrator_list_search_RateLimitError_raises_http_exception(mocker):
    mocker.patch(
        "packages.data_provider.src.data_provider.DataProvider.get_abstract_from_doi",
        side_effect=RateLimitError(time.time() + 10),
    )

    with pytest.raises(HTTPException):
        Orchestrator.list_search([("doi", ["12345"])])


def test_orchestrator_list_search_RateLimitError_raises_ratelimit_then_http_exception(
    mocker,
):
    Orchestrator.time_start = time.time() + 60
    with pytest.raises(HTTPException):
        Orchestrator.list_search([("doi", ["12345"])])


def test_orchestrator_search_error_404_empty_ontology(mocker):
    mocker.patch(
        "packages.techniques_extractor.src.techniques_extractor.Llm.llm_run",
        return_value='{"techniques":["xfas"]}',
    )

    mocker.patch(
        "packages.panet_technique_matcher.src.panet_technique_matcher.MatchMapper.map_to_panet",
        side_effect=EmptyOntologyError,
    )
    with pytest.raises(HTTPException):
        Orchestrator.search(
            "This is a test to check if error 404 is raised when the ontology is empty"
        )


def test_orchestrator_search_error_404_ontology_not_found(mocker):
    mocker.patch(
        "packages.techniques_extractor.src.techniques_extractor.Llm.llm_run",
        return_value='{"techniques":["xfas"]}',
    )

    mocker.patch(
        "packages.panet_technique_matcher.src.panet_technique_matcher.MatchMapper.map_to_panet",
        side_effect=OntologyNotFoundError,
    )
    with pytest.raises(HTTPException):
        Orchestrator.search(
            "This is a test to check if error 404 is raised when the ontology is not found"
        )
