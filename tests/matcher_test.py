from packages.panet_technique_matcher.src.panet_technique_matcher.matchmapper import (
    MatchMapper,
)
from packages.panet_technique_matcher.src.panet_technique_matcher.ontology_importer import (
    Ontology,
)
import unittest


class TestClass(unittest.TestCase):
    my_ontology = None

    @classmethod
    def setup_class(cls):
        cls.my_ontology = Ontology.getting_ontology()

    @classmethod
    def teardown_class(cls):
        cls.my_ontology = None

    def test_matcher_found(self):
        assert MatchMapper.my_matcher("diffraction", self.my_ontology)["n_first"][
            0
        ] == {
            "technique": {
                "label": "diffraction",
                "altLabel": [],
                "subClassOf": {"PaNET01020": "elastic scattering"},
                "definition1": "",
                "definition2": "https://en.wikipedia.org/wiki/Diffraction",
                "id": "http://purl.org/pan-science/PaNET/PaNET01022",
            },
            "score": 0.0,
        }

    def test_matcher_almost_found(self):
        result = MatchMapper.my_matcher("JISANS", self.my_ontology)
        assert result["n_first"][1]["score"] == 0.1667
        assert result["n_first"][0] == {
            "technique": {
                "label": "grazing incidence small angle neutron scattering",
                "altLabel": ["GISANS"],
                "subClassOf": {
                    "PaNET01099": "grazing incidence small angle scattering",
                    "PaNET01189": "small angle neutron scattering",
                },
                "definition1": "",
                "definition2": "https://en.wikipedia.org/wiki/Grazing-incidence_small-angle_scattering",
                "id": "http://purl.org/pan-science/PaNET/PaNET01276",
            },
            "score": 0.1667,
        }

    def test_matcher_not_found(self):
        assert MatchMapper.my_matcher("19", self.my_ontology) is None

    def test_matcher_empty_list(self):
        assert MatchMapper.my_matcher("EXAFS", []) is None

    def test_matcher_empty_input(self):
        assert MatchMapper.my_matcher("", self.my_ontology) is None

    # def test_map_to_panet_exception(self):
    #     with self.assertRaises(JSONDecodeError):
    #         MatchMapper.map_to_panet("!")
