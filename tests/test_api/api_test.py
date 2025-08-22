from fastapi.testclient import TestClient
from src.panetextractor.api.main import app
from unittest.mock import Mock
import pytest
import time


def test_get_techniques_success():
    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/extract_techniques/?input=In%20this%20contribution%20small-angle%20scattering%20from%20layered%20systems%20is%20%20considered.%20When%20a%20colloidal%20dispersion%20is%20stirred%20it%20usually%20decomposes%20%20into%20layers.%20There%20are%20two%20important%20questions%20concerning%20these%20layers%3A%20%20What%20is%20the%20structure%20in%20a%20layer%3F%20What%20is%20the%20stacking%20structure%20%20between%20such%20layers%3F%20For%20concentrated%20colloidal%20dispersions%20both%20these%20%20questions%20can%20be%20investigated%20by%20small-angle%20scattering%20experiments.%20It%20%20will%20become%20apparent%20that%20the%20answer%20is%20also%20important%20for%20technical%20%20applications.%20Both%20a%20theoretical%20description%20as%20well%20as%20an%20experimental%20%20verification%20are%20given%20in%20the%20paper%22%20QUERY_2%20%3D%20%22NiFe-layered%20double%20hydroxides%20%28LDHs%29%20are%20promising%20electrocatalysts%20for%20the%20oxygen%20evolution%20reaction%20%28OER%29%20in%20alkaline%20media.%20Here%2C%20operando%20X-ray%20diffraction%20%28XRD%29%20and%20X-ray%20total%20scattering%20are%20used%20with%20Pair%20Distribution%20Function%20%28PDF%29%20analysis%20to%20investigate%20the%20atomic%20structure%20of%20the%20catalytically%20active%20material%20and%20follow%20structural%20changes%20under%20operating%20conditions.%20XRD%20shows%20an%20interlayer%20contraction%20under%20applied%20oxidative%20potential%2C%20which%20relates%20to%20a%20transition%20from%20the%20%CE%B1-LDH%20to%20the%20%CE%B3-LDH%20phase.%20The%20phase%20transition%20is%20reversible%2C%20and%20the%20%CE%B1-LDH%20structure%20is%20recovered%20at%201.3%20VRHE.%20However%2C%20PDF%20analysis%20shows%20an%20irreversible%20increase%20in%20the%20stacking%20disorder%20under%20operating%20conditions%2C%20along%20with%20a%20decrease%20in%20the%20LDH%20sheet%20size.%20The%20analysis%20thus%20shows%20that%20the%20operating%20conditions%20induce%20a%20breakdown%20of%20the%20particles%20leading%20to%20a%20decrease%20in%20crystallite%20size.",
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        assert response.status_code == 200


def test_input_is_too_short():
    with TestClient(app) as client:
        response = client.post("http://127.0.0.1:8000/extract_techniques/?input=a")
        assert response.status_code == 422


def test_input_is_too_long():
    with TestClient(app) as client:
        response = client.post(
            "http://127.0.0.1:8000/extract_techniques/?input=Zeolitic%20imidazolate%20frameworks%20(ZIFs)1%2C2%20are%20a%20class%20of%20metal%E2%80%93organic%20frameworks%20(MOFs)%20that%20hold%20promise%20for%20applications%20in%20molecular%20separations3%2C4%2C5%2C6%2C7%2C8%2C%20patterning9%2C10%20and%20sensing11.%20Their%20chemical%20and%20physical%20properties%20have%20been%20widely%20explored%20as%20a%20function%20of%20framework%20flexibility12%2C13%2C14%2C15%20as%20well%20as%20structural%20defects16%2C17.%20The%20realization%20of%20two-dimensional%20(2D)%20ZIF%20films%20with%20thickness%20down%20to%20that%20afforded%20by%20a%20single%20structural%20building%20unit%20is%20highly%20desired%20to%20make%20ZIF%20analogues%20to%20graphene%20and%20related%202D%20materials%20with%20an%20added%20advantage%3A%20the%20intrinsic%20nanoporosity%20of%20ZIF%20can%20be%20used%20to%20separate%20molecules%20and%20maximize%20the%20permselective%20flux18.%20However%2C%20the%20realization%20of%202D%20crystalline%20and%20ultrathin%20amorphous%20ZIF%20films%20has%20remained%20elusive.%20Although%20layered%20ZIFs%20such%20as%20ZIF-L%20(ref.%2019)%2C%20Zn2(bim)4%20(ref.%2020)%20and%20analogues21%20have%20been%20reported%2C%20individual%20ZIF%20layers%20in%20these%20materials%20have%20a%20small%20aspect%20ratio%2C%20which%20prevents%20the%20realization%20of%20continuous%202D%20ZIF%20films%20with%20structural%20uniformity%20over%20a%20macroscopic%20(for%20example%2C%20wafer)%20length%20scale.%20State-of-the-art%20ZIF%20deposition%20methods%20yield%20polycrystalline%20films%20with%20thickness%20larger%20than%2050%E2%80%89nm%20(refs.%2022%2C23%2C24%2C25).%20This%20is%20mainly%20due%20to%20difficulty%20in%20achieving%20in-plane%20film%20growth%20without%20film%20thickening.%0A%0AConsiderable%20knowledge%20exists%20on%20ZIF%2FMOF%20crystal%20nucleation%20and%20growth%20in%20solution26%2C27%2C28%2C29%2C30%2C31.%20Based%20on%20data%20from%20synchrotron%20X-ray%20scattering%2C%20density%20functional%20theory%20(DFT)%20and%20molecular%20dynamics%20simulations%2C%20as%20well%20as%20other%20techniques%2C%20it%20is%20generally%20accepted%20that%20ZIF%20formation%20involves%20a%20sequence%20of%20events%20starting%20from%20the%20formation%20of%20small%20(~1%E2%80%89nm)%20metastable%20prenucleation%20clusters%2C%20which%20evolve%20through%20aggregation%20followed%20by%20intra-aggregate%20ZIF%20nucleation%20and%20growth.%20Recent%20studies%20on%20surface-directed%20MOF%20growth32%2C33%2C34%2C35%2C36%2C37%2C38%2C39%2C40%20indicate%20that%20the%20diffusion%20of%20MOF%20precursors%20in%20the%20vicinity%20of%20the%202D%20material%20and%20MOF%E2%80%932D%20material%20interactions%20are%20key%20to%20regulate%20the%20crystallinity%20of%20the%20MOF%20film%20and%20the%20ability%20to%20maintain%20in-plane%2Fhorizontal%20growth%20(desired%20for%20ultrathin%20films)%20versus%20out-of-plane%2Fvertical%20(undesired)%20growth.%0A%0AHere%20we%20report%20macroscopically%20uniform%202D%20ZIF%20films%20with%20exquisite%20nanometre-scale%20control%20over%20the%20film%20thickness%20by%20suppressing%20the%20out-of-plane%20growth%20by%20using%20an%20ultradilute%20growth%20solution.%20The%20ultralow%20precursor%20concentration%20restricts%20homogeneous%20nucleation%20in%20the%20solution%20and%20facilitates%20the%20growth%20of%20nanometre-thick%20films%20over%20an%20immersed%20substrate%20with%20deposition%20timescales%20of%20a%20few%20minutes.%20The%20film%20crystallinity%20is%20determined%20by%20the%20interaction%20of%20molecular%20precursors%20with%20the%20substrate%20ranging%20from%20substrate-registry-determined%20order%20to%20amorphous%20films%20in%20the%20absence%20of%20any%20crystallographic%20registry.%20The%20film%20thickness%20could%20be%20controlled%20with%20a%20resolution%20of%20a%20single%20layer%20by%20controlling%20the%20deposition%20time%20and%20number%20of%20coatings."
        )
        assert response.status_code == 422


def test_invalid_accept_header():
    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/extract_techniques/?input=In%20this%20contribution%20small-angle%20scattering%20from%20layered%20systems%20is%20%20considered.%20When%20a%20colloidal%20dispersion%20is%20stirred%20it%20usually%20decomposes%20%20into%20layers.%20There%20are%20two%20important%20questions%20concerning%20these%20layers%3A%20%20What%20is%20the%20structure%20in%20a%20layer%3F%20What%20is%20the%20stacking%20structure%20%20between%20such%20layers%3F%20For%20concentrated%20colloidal%20dispersions%20both%20these%20%20questions%20can%20be%20investigated%20by%20small-angle%20scattering%20experiments.%20It%20%20will%20become%20apparent%20that%20the%20answer%20is%20also%20important%20for%20technical%20%20applications.%20Both%20a%20theoretical%20description%20as%20well%20as%20an%20experimental%20%20verification%20are%20given%20in%20the%20paper%22%20QUERY_2%20%3D%20%22NiFe-layered%20double%20hydroxides%20%28LDHs%29%20are%20promising%20electrocatalysts%20for%20the%20oxygen%20evolution%20reaction%20%28OER%29%20in%20alkaline%20media.%20Here%2C%20operando%20X-ray%20diffraction%20%28XRD%29%20and%20X-ray%20total%20scattering%20are%20used%20with%20Pair%20Distribution%20Function%20%28PDF%29%20analysis%20to%20investigate%20the%20atomic%20structure%20of%20the%20catalytically%20active%20material%20and%20follow%20structural%20changes%20under%20operating%20conditions.%20XRD%20shows%20an%20interlayer%20contraction%20under%20applied%20oxidative%20potential%2C%20which%20relates%20to%20a%20transition%20from%20the%20%CE%B1-LDH%20to%20the%20%CE%B3-LDH%20phase.%20The%20phase%20transition%20is%20reversible%2C%20and%20the%20%CE%B1-LDH%20structure%20is%20recovered%20at%201.3%20VRHE.%20However%2C%20PDF%20analysis%20shows%20an%20irreversible%20increase%20in%20the%20stacking%20disorder%20under%20operating%20conditions%2C%20along%20with%20a%20decrease%20in%20the%20LDH%20sheet%20size.%20The%20analysis%20thus%20shows%20that%20the%20operating%20conditions%20induce%20a%20breakdown%20of%20the%20particles%20leading%20to%20a%20decrease%20in%20crystallite%20size.",
            headers={"Content-type": "application/json", "Accept": "application/xhtml"},
        )
        assert response.status_code == 406


def test_invalid_accept_header_2():
    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/dois_to_techniques/",
            headers={"Content-type": "application/json", "Accept": "application/xhtml"},
            json={"dois": ["12345"]},
        )
        assert response.status_code == 406


@pytest.fixture
def mock_rate_limit_error_openaire(mocker):
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
        mock_response.headers = {"Retry-After": "5"}
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


def test_rate_time_limit_openaire(mock_rate_limit_error_openaire):
    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/dois_to_techniques/",
            json={"dois": ["12345678910"]},
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        assert response.status_code == 429


def test_rate_time_limit_and_retried_before_given_time(mock_rate_limit_error_openaire):
    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/dois_to_techniques/",
            json={"dois": ["12345678910"]},
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        time.sleep(1)
        response = client.post(
            url="http://127.0.0.1:8000/dois_to_techniques/",
            json={"dois": ["12345678910"]},
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        assert response.status_code == 429
        assert response.headers.get("Retry-After") == str(3)
