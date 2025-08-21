from packages.data_provider.src.data_provider import (
    DataProvider,
    AbstractImportError,
    RateLimitError,
)
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_rate_limit_error_without_retry_after(mocker):
    """Fixture to mock an error 429 response"""

    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = []
    mock_response.json.return_value = {"error": "Too many requests"}

    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )

    return mock_response


@pytest.fixture
def mock_rate_limit_error_with_retry_after(mocker):
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = {"Retry-After": "2"}
    mock_response.json.return_value = {"error": "Too many requests"}

    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )

    return mock_response


def test_found_from_doi():
    DataProvider()
    response = DataProvider.call_open_aire("10.1038/s41563-023-01669-z")
    assert response.json()["header"]["numFound"] == 1
    assert (
        response.json()["results"][0]["mainTitle"]
        == "Unit-cell-thick zeolitic imidazolate framework films for membrane application"
    )


def test_nothing_found_from_doi():
    with pytest.raises(AbstractImportError):
        DataProvider()
        DataProvider.call_open_aire("10.4466/123s132111")


def test_input_a_void_doi_get_all_products():
    DataProvider()
    response = DataProvider.call_open_aire("")
    assert response.json()["header"]["numFound"] > 1


def test_rate_limit_error_retry_after(mock_rate_limit_error_with_retry_after):
    with pytest.raises(RateLimitError):
        DataProvider.call_open_aire("10.1038/s41563-023-01669-z")


def test_rate_limit_error_without_retry_after(
    mock_rate_limit_error_without_retry_after,
):
    with pytest.raises(RateLimitError):
        DataProvider.call_open_aire("10.1038/s41563-023-01669-z")


def test_get_abstract_doi_success():
    DataProvider()
    result = DataProvider.get_abstract_from_doi("10.1038/s41563-023-01669-z")

    assert (
        result
        == "<jats:title>Abstract</jats:title><jats:p>Zeolitic imidazolate frameworks (ZIFs) are a subset of metal–organic frameworks with more than 200 characterized crystalline and amorphous networks made of divalent transition metal centres (for example, Zn<jats:sup>2+</jats:sup> and Co<jats:sup>2+</jats:sup>) linked by imidazolate linkers. ZIF thin films have been intensively pursued, motivated by the desire to prepare membranes for selective gas and liquid separations. To achieve membranes with high throughput, as in ångström-scale biological channels with nanometre-scale path lengths, ZIF films with the minimum possible thickness—down to just one unit cell—are highly desired. However, the state-of-the-art methods yield membranes where ZIF films have thickness exceeding 50 nm. Here we report a crystallization method from ultradilute precursor mixtures, which exploits registry with the underlying crystalline substrate, yielding (within minutes) crystalline ZIF films with thickness down to that of a single structural building unit (2 nm). The film crystallized on graphene has a rigid aperture made of a six-membered zinc imidazolate coordination ring, enabling high-permselective H<jats:sub>2</jats:sub> separation performance. The method reported here will probably accelerate the development of two-dimensional metal–organic framework films for efficient membrane separation.</jats:p>"
    )


def test_get_registry_agency_success(mocker):
    doi = "12345"
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{"doi": "12345", "RA": "testCrossref"}]
    mock_response.status_code = 200
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )
    response = DataProvider.get_registry_agency(doi)
    assert response == "testCrossref"


def test_get_registry_agency_error(mocker):
    doi = "12345"
    mock_response = mocker.Mock()
    mock_response.json.return_value = [{"doi": "12345", "status": "Invalid DOI"}]
    mock_response.status_code = 200
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )
    with pytest.raises(AbstractImportError):
        DataProvider.get_registry_agency(doi)


def test_call_datacite_success(mocker):
    doi = "12345"
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": doi,
                "type": "dois",
                "attributes": {"descriptions": [{"description": "test"}]},
            }
        ],
        "meta": {},
    }
    mock_response.status_code = 200
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )
    response = DataProvider.call_datacite(doi)
    assert response["data"][0]["id"] == doi


def test_get_abstract_doi_no_abstract(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "header": {"numFound": 1},
        "results": [{"mainTitle": "some title", "subTitle": None}],
    }
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.DataProvider.call_open_aire",
        return_value=mock_response,
    )

    mock_ra = mocker.Mock()
    mock_ra.json.return_value = [{"doi": "12345", "RA": "Crossref"}]
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.DataProvider.get_registry_agency",
        return_value=mock_ra,
    )

    DataProvider()
    result = DataProvider.get_abstract_from_doi("12345")

    assert result == "No abstract available"


def test_get_abstract_doi_abstract_import_error(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )
    result = DataProvider.get_abstract_from_doi("12345")

    assert result == "Error: No abstract available"


@pytest.fixture
def mock_rate_limit_error_openaire_test_without_retry_after(mocker):
    def mock_datacite(url):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "data": [{"attributes": {"descriptions": [{"description": "Test"}]}}]
        }
        mock_response.status_code = 200
        return mock_response

    def mock_openaire(url, headers=None):
        mock_response = mocker.Mock()
        mock_response.status_code = 429
        mock_response.headers = {}
        mock_response.json.return_value = {"error": "Too many requests"}
        return mock_response

    def mock_doiRA(url):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"doi": "12345", "RA": "Crossref"}]
        return mock_response

    def side_effect(url, headers=None):
        if "openaire" in url:
            return mock_openaire(url, headers)
        elif "datacite" in url:
            return mock_datacite(url)
        elif "doi.org" in url:
            return mock_doiRA(url)

    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        side_effect=side_effect,
    )


def test_get_abstract_doi_rate_limit_error(
    mock_rate_limit_error_openaire_test_without_retry_after,
):
    with pytest.raises(RateLimitError):
        DataProvider.get_abstract_from_doi("12345")


def test_token_error(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )
    with pytest.raises(AbstractImportError):
        DataProvider()


def test_call_datacite_error(mocker):
    doi = "12345"
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"title": ""}
    mock_response.status_code = 400
    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        return_value=mock_response,
    )
    with pytest.raises(AbstractImportError):
        DataProvider.call_datacite(doi)


def test_get_abstract_from_doi_datacite_success(mocker):
    doi = "12345"

    def mock_datacite(url):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "attributes": {
                        "descriptions": [
                            {"description": "Test_get_abstract_datacite_success"}
                        ]
                    }
                }
            ]
        }
        mock_response.status_code = 200
        return mock_response

    def mock_doiRA(url):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"doi": "12345", "RA": "DataCite"}]
        return mock_response

    def side_effect(url, headers=None):
        if "datacite" in url:
            return mock_datacite(url)
        elif "doi.org" in url:
            return mock_doiRA(url)

    mocker.patch(
        "packages.data_provider.src.data_provider.data_provider.requests.get",
        side_effect=side_effect,
    )

    response = DataProvider.get_abstract_from_doi(doi)
    assert response == "Test_get_abstract_datacite_success"


def test_get_abstract_from_doi_datacite_error():
    pass
