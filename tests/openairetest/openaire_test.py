from src.openaire import OpenAire,AbstractImportError
import pytest

def test_found_from_doi():
    response = OpenAire.get_abstract_from_doi("10.1038/s41563-023-01669-z")
    assert response.json()['header']['numFound'] == 1
    assert response.json()['results'][0]['mainTitle'] == "Unit-cell-thick zeolitic imidazolate framework films for membrane application"

def test_nothing_found_from_doi():
    with pytest.raises(AbstractImportError):
        OpenAire.get_abstract_from_doi("10.4466/123s132111")

def test_input_a_void_doi_get_all_products():
    response = OpenAire.get_abstract_from_doi("")
    assert response.json()['header']['numFound'] >1