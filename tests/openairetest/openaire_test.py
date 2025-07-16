from src.openaire import OpenAire,AbstractImportError,RateLimitError
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_rate_limit_error_with_retry_after(mocker):
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = {"Retry-After": "2"}
    mock_response.json.return_value = {"error": "Too many requests"}
    
    mocker.patch("src.openaire.openaireapi.OpenAire.requests.get", return_value=mock_response)

    return mock_response

@pytest.fixture
def mock_rate_limit_error_without_retry_after(mocker):
    """Fixture to mock an error 429 response"""

    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = []
    mock_response.json.return_value = {"error": "Too many requests"}


    mocker.patch("src.openaire.openaireapi.OpenAire.requests.get", return_value=mock_response)

    return mock_response




def test_found_from_doi():
    response = OpenAire.call_open_aire("10.1038/s41563-023-01669-z")
    assert response.json()['header']['numFound'] == 1
    assert response.json()['results'][0]['mainTitle'] == "Unit-cell-thick zeolitic imidazolate framework films for membrane application"

def test_nothing_found_from_doi():
    with pytest.raises(AbstractImportError):
        OpenAire.call_open_aire("10.4466/123s132111")

def test_input_a_void_doi_get_all_products():
    response = OpenAire.call_open_aire("")
    assert response.json()['header']['numFound'] >1

def test_rate_limit_error_retry_after(mock_rate_limit_error_with_retry_after):
    with pytest.raises(RateLimitError):
        OpenAire.call_open_aire("10.1038/s41563-023-01669-z")

def test_rate_limit_error_without_retry_after(mock_rate_limit_error_without_retry_after):
    with pytest.raises(RateLimitError):
        OpenAire.call_open_aire("10.1038/s41563-023-01669-z")



def test_get_abstract_doi_success():
    result = OpenAire.get_abstract_from_doi("10.1038/s41563-023-01669-z")

    assert result == "<jats:title>Abstract</jats:title><jats:p>Zeolitic imidazolate frameworks (ZIFs) are a subset of metal–organic frameworks with more than 200 characterized crystalline and amorphous networks made of divalent transition metal centres (for example, Zn<jats:sup>2+</jats:sup> and Co<jats:sup>2+</jats:sup>) linked by imidazolate linkers. ZIF thin films have been intensively pursued, motivated by the desire to prepare membranes for selective gas and liquid separations. To achieve membranes with high throughput, as in ångström-scale biological channels with nanometre-scale path lengths, ZIF films with the minimum possible thickness—down to just one unit cell—are highly desired. However, the state-of-the-art methods yield membranes where ZIF films have thickness exceeding 50 nm. Here we report a crystallization method from ultradilute precursor mixtures, which exploits registry with the underlying crystalline substrate, yielding (within minutes) crystalline ZIF films with thickness down to that of a single structural building unit (2 nm). The film crystallized on graphene has a rigid aperture made of a six-membered zinc imidazolate coordination ring, enabling high-permselective H<jats:sub>2</jats:sub> separation performance. The method reported here will probably accelerate the development of two-dimensional metal–organic framework films for efficient membrane separation.</jats:p>"


def test_get_abstract_doi_no_abstract(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"header":{"numFound":1},"results":[{"mainTitle":"some title","subTitle":None}]}
    mocker.patch("src.openaire.openaireapi.OpenAire.call_open_aire",return_value = mock_response)
    result = OpenAire.get_abstract_from_doi("12345")

    assert result == "No abstract available"

def test_get_abstract_doi_abstract_import_error(mocker):

    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch("src.openaire.openaireapi.OpenAire.requests.get", return_value=mock_response)

    result = OpenAire.get_abstract_from_doi("12345")

    assert result == "No abstract available"

def test_get_abstract_doi_rate_limit_error(mock_rate_limit_error_without_retry_after):
    with pytest.raises(RateLimitError):
        OpenAire.get_abstract_from_doi("12345")
