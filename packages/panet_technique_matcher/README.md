# panet-technique-matcher
---
## The panet-technique-matcher consists of 3 modules:
ontology_importer,matchmapper,score

 I.`score` uses rapifuzz's normalized distance functions
1. **get_normalized_distance** : get normalized distance between two strings
2. **get_altalabels_normalized_distance** : get normalized distance between a string and a each string of a list of string

 II.`ontology_importer` uses owlready2 to load the paNET ontology 
1. **getting_ontology** : import the paNET ontology and return it as a list of dictionaries
2. **extract_subclass_of** : extract the superclasses of a class from the original ontology , name and label only

 III.`the matchmapper` has two functions, 
1. **my_matcher** : matches a string to the closest paNET terms and pick up to ten or n of the best matches, if nothing close enough return None
2. **map_to_panet** : read a json with a list of string and match each to a paNET techniques

## Usage
```console
    > import rapidfuzz
    > from panet_technique_matcher import Score,Ontology,MatchMapper
```   


#### get_normalized_distance
```console   
   > print(Score.get_normalized_distance("abc","a",rapidfuzz.distance.Levenshtein.normalized_distance))
    0.6667
```

#### get_altalabels_normalized_distance
```console
   > print(Score.get_altlabels_normalized_distances("abc",["abcd","abcde"],rapidfuzz.distance.Levenshtein.normalized_distance))
    [0.25, 0.4]
```


#### getting_ontology
```console   
    > Ontology.getting_ontology()
```

#### extract_subclass_of
```console   
   > Ontology.extract_subclass_of(a_class)
```


#### my_matcher
```console   
   > print(MatchMapper.my_matcher("XAFS",[{"label": "x-ray absorption fine structure", "altLabel": ["XAFS"]},{"label": "pair distribution function", "altLabel": ["PDF"]},]))
{'ten first': [{'technique': {'label': 'x-ray absorption fine structure', 'altLabel': ['XAFS']}, 'score': 0.0}, {'technique': {'label': 'pair distribution function', 'altLabel': ['PDF']}, 'score': 0.75}]}
```

#### map_to_panet
```console   
   > print(MatchMapper.map_to_panet({"techniques":["small angle scattering"]}))
[{'inText': 'small angle scattering', 'inPaNET': {'technique': {'id': 'http://purl.org/pan-science/PaNET/PaNET01124', 'label': 'small angle scattering', 'altLabel': ['SAS', 'small angle diffraction'], 'subClassOf': {'PaNET01037': 'low momentum transfer scattering'}, 'definition1': '', 'definition2': 'https://en.wikipedia.org/wiki/Small-angle_scattering'}, 'score': 0.0}}]
```


