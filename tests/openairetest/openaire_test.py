from src.openaire import OpenAire,AbstractImportError,RateLimitError
import pytest
from unittest.mock import Mock

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

@pytest.fixture
def mock_rate_limit_error(mocker):
    """Fixture to mock an error 429 response"""

    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = {"Retry-After": "2"}
    mock_response.json.return_value = {"error": "Too many requests"}


    mocker.patch("src.openaire.openaireapi.OpenAire.requests.get", return_value=mock_response)

    return mock_response

@pytest.fixture
def mock_rate_limit_error_2(mocker):
    """Fixture to mock an error 429 response"""

    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = []
    mock_response.json.return_value = {"error": "Too many requests"}


    mocker.patch("src.openaire.openaireapi.OpenAire.requests.get", return_value=mock_response)

    return mock_response

def test_rate_limit_error_retry_after(mock_rate_limit_error):
    with pytest.raises(RateLimitError):
        OpenAire.call_open_aire("10.1038/s41563-023-01669-z")

def test_rate_limit_error_without_retry_after(mock_rate_limit_error_2):
    with pytest.raises(RateLimitError):
        OpenAire.call_open_aire("10.1038/s41563-023-01669-z")

#def test_invalid_access_token