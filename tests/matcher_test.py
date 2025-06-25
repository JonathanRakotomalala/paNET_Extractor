from src.matchmapper.matchmapper import MatchMapper
from src.ontology.ontology_import import Ontology
import unittest


class TestClass(unittest.TestCase) :

    my_ontology = None

    @classmethod
    def setup_class(cls):
        cls.my_ontology = Ontology.getting_ontology()

    @classmethod
    def teardown_class(cls):
        cls.my_ontology = None


    def test_matcher_found(self):
        assert MatchMapper.my_matcher("diffraction",self.my_ontology)["ten first"][0]=={'technique': {'label': 'diffraction', 'altLabel': [], 'subClassOf': {'PaNET01020': 'elastic scattering'}, 'definition1': '', 'definition2': 'https://en.wikipedia.org/wiki/Diffraction'}, 'distance': 0.0}

    def test_matcher_almost_found(self):
        result= MatchMapper.my_matcher("JISANS",self.my_ontology)
        assert result["ten first"][1]['distance'] == 0.1667
        assert result["ten first"][0]=={"technique":{"label":"grazing incidence small angle neutron scattering","altLabel":["GISANS"],'subClassOf':{'PaNET01099':'grazing incidence small angle scattering','PaNET01189':'small angle neutron scattering'},'definition1': '', 'definition2':'https://en.wikipedia.org/wiki/Grazing-incidence_small-angle_scattering'},"distance":0.1667}


    def test_matcher_not_found(self):
        assert MatchMapper.my_matcher("19",self.my_ontology)=={"ten first":None}

    def test_matcher_empty_list(self):

        assert MatchMapper.my_matcher("EXAFS",[])=={"ten first":None}

    def test_matcher_empty_input(self):
        assert MatchMapper.my_matcher("",self.my_ontology)=={"ten first":None}

    # def test_map_to_panet_exception(self):
    #     with self.assertRaises(JSONDecodeError):
    #         MatchMapper.map_to_panet("!")
