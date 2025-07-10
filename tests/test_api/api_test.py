from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import Mock
import pytest
from fastapi import HTTPException
from src.openaire import OpenAire

def test_technic_working():
    with TestClient(app) as client:
        response = client.post(url=
            "http://127.0.0.1:8000/extract_techniques/?input=In%20this%20contribution%20small-angle%20scattering%20from%20layered%20systems%20is%20%20considered.%20When%20a%20colloidal%20dispersion%20is%20stirred%20it%20usually%20decomposes%20%20into%20layers.%20There%20are%20two%20important%20questions%20concerning%20these%20layers%3A%20%20What%20is%20the%20structure%20in%20a%20layer%3F%20What%20is%20the%20stacking%20structure%20%20between%20such%20layers%3F%20For%20concentrated%20colloidal%20dispersions%20both%20these%20%20questions%20can%20be%20investigated%20by%20small-angle%20scattering%20experiments.%20It%20%20will%20become%20apparent%20that%20the%20answer%20is%20also%20important%20for%20technical%20%20applications.%20Both%20a%20theoretical%20description%20as%20well%20as%20an%20experimental%20%20verification%20are%20given%20in%20the%20paper%22%20QUERY_2%20%3D%20%22NiFe-layered%20double%20hydroxides%20%28LDHs%29%20are%20promising%20electrocatalysts%20for%20the%20oxygen%20evolution%20reaction%20%28OER%29%20in%20alkaline%20media.%20Here%2C%20operando%20X-ray%20diffraction%20%28XRD%29%20and%20X-ray%20total%20scattering%20are%20used%20with%20Pair%20Distribution%20Function%20%28PDF%29%20analysis%20to%20investigate%20the%20atomic%20structure%20of%20the%20catalytically%20active%20material%20and%20follow%20structural%20changes%20under%20operating%20conditions.%20XRD%20shows%20an%20interlayer%20contraction%20under%20applied%20oxidative%20potential%2C%20which%20relates%20to%20a%20transition%20from%20the%20%CE%B1-LDH%20to%20the%20%CE%B3-LDH%20phase.%20The%20phase%20transition%20is%20reversible%2C%20and%20the%20%CE%B1-LDH%20structure%20is%20recovered%20at%201.3%20VRHE.%20However%2C%20PDF%20analysis%20shows%20an%20irreversible%20increase%20in%20the%20stacking%20disorder%20under%20operating%20conditions%2C%20along%20with%20a%20decrease%20in%20the%20LDH%20sheet%20size.%20The%20analysis%20thus%20shows%20that%20the%20operating%20conditions%20induce%20a%20breakdown%20of%20the%20particles%20leading%20to%20a%20decrease%20in%20crystallite%20size."
            ,headers={"Content-type": "application/json", "Accept": "application/json"}

        )
        assert response.status_code == 200


def test_too_short():
    with TestClient(app) as client:
        response = client.post("http://127.0.0.1:8000/extract_techniques/?input=a")
        assert response.status_code == 422


def test_invalid_accept_header():
    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/extract_techniques/?input=In%20this%20contribution%20small-angle%20scattering%20from%20layered%20systems%20is%20%20considered.%20When%20a%20colloidal%20dispersion%20is%20stirred%20it%20usually%20decomposes%20%20into%20layers.%20There%20are%20two%20important%20questions%20concerning%20these%20layers%3A%20%20What%20is%20the%20structure%20in%20a%20layer%3F%20What%20is%20the%20stacking%20structure%20%20between%20such%20layers%3F%20For%20concentrated%20colloidal%20dispersions%20both%20these%20%20questions%20can%20be%20investigated%20by%20small-angle%20scattering%20experiments.%20It%20%20will%20become%20apparent%20that%20the%20answer%20is%20also%20important%20for%20technical%20%20applications.%20Both%20a%20theoretical%20description%20as%20well%20as%20an%20experimental%20%20verification%20are%20given%20in%20the%20paper%22%20QUERY_2%20%3D%20%22NiFe-layered%20double%20hydroxides%20%28LDHs%29%20are%20promising%20electrocatalysts%20for%20the%20oxygen%20evolution%20reaction%20%28OER%29%20in%20alkaline%20media.%20Here%2C%20operando%20X-ray%20diffraction%20%28XRD%29%20and%20X-ray%20total%20scattering%20are%20used%20with%20Pair%20Distribution%20Function%20%28PDF%29%20analysis%20to%20investigate%20the%20atomic%20structure%20of%20the%20catalytically%20active%20material%20and%20follow%20structural%20changes%20under%20operating%20conditions.%20XRD%20shows%20an%20interlayer%20contraction%20under%20applied%20oxidative%20potential%2C%20which%20relates%20to%20a%20transition%20from%20the%20%CE%B1-LDH%20to%20the%20%CE%B3-LDH%20phase.%20The%20phase%20transition%20is%20reversible%2C%20and%20the%20%CE%B1-LDH%20structure%20is%20recovered%20at%201.3%20VRHE.%20However%2C%20PDF%20analysis%20shows%20an%20irreversible%20increase%20in%20the%20stacking%20disorder%20under%20operating%20conditions%2C%20along%20with%20a%20decrease%20in%20the%20LDH%20sheet%20size.%20The%20analysis%20thus%20shows%20that%20the%20operating%20conditions%20induce%20a%20breakdown%20of%20the%20particles%20leading%20to%20a%20decrease%20in%20crystallite%20size.",
            headers={"Content-type": "application/json", "Accept": "application/xhtml"},
        )
        assert response.status_code == 406


@pytest.fixture
def mock_rate_limit_error(mocker):
    """Fixture to mock an error 429 response"""

    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.headers = {"Retry-After": "2"}
    mock_response.json.return_value = {"error": "Too many requests,retry later"}


    mocker.patch("src.openaire.openaireapi.OpenAire.requests.get", return_value=mock_response)

    return mock_response


def test_rate_time_limit(mock_rate_limit_error):

    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/dois_to_techniques/",json={"dois":["12345678910"]},
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        assert response.status_code == 429