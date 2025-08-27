# panet-technique-matcher
---
<p align="center">
 <a href="https://www.python.org">
<img src="https://img.shields.io/badge/python->=3.10-blue"> 
</a>
</p>

## The panet-technique-matcher consists of 3 modules:
ontology_importer,matchmapper,score

 I.`score` uses rapifuzz's normalized distance functions
1. **get_normalized_distance** : gets normalized distance between two strings
2. **get_altalabels_normalized_distance** : calculates normalized distance between a string and a each string of a list of string

 II.`ontology_importer` uses owlready2 to load the paNET ontology 
1. **fetch_ontology** : imports the paNET ontology and return it as a list of dictionaries

 III.`the matchmapper` 
1. **my_matcher** : matches a string to the closest paNET terms and pick up to ten or n of the best matches, if nothing close enough return None
2. **map_to_panet** : reads a json with a list of string and match each to a paNET techniques using function from the distance module of rapidfuzz (2 algorithms available : levenshtein (default) and indel)

 VI.`superclass extractor` 
1. **extract_subclass_of** : extracts the superclasses of a class


## Usage
```console
> import rapidfuzz
> from panet_technique_matcher import Score,Ontology,MatchMapper
```   


#### get_normalized_distance
Using rapidfuzz distance calculation algorithms. 
```console   
> score = Score.get_normalized_distance("abc","a",rapidfuzz.distance.Levenshtein.normalized_distance)
> print(score)
   0.6667
```

#### get_altalabels_normalized_distance
Map of a list with rapidfuzz distance calculation algorithms
```console
> scores = Score.get_altlabels_normalized_distances("abc",["abcd","abcde"],rapidfuzz.distance.Levenshtein.normalized_distance)
> print(scores)
[0.25, 0.4]
```


#### fetch_ontology
With owlready2, loads the paNET ontology 
```console   
> ontology = Ontology.fetch_ontology()
```

#### my_matcher
compares a technique(string) with all paNET terms
```console   
> matches = MatchMapper.my_matcher("XAFS",[{"label": "x-ray absorption fine structure", "altLabel": ["XAFS"]},{"label": "pair distribution function", "altLabel": ["PDF"]},])
> print(matches)
{'n first': [{'technique': {'label': 'x-ray absorption fine structure', 'altLabel': ['XAFS']}, 'score': 0.0}, {'technique': {'label': 'pair distribution function', 'altLabel': ['PDF']}, 'score': 0.75}]}
```

#### map_to_panet
compares list of techniques (json) with all paNET terms
```console   
> matches = MatchMapper.map_to_panet({"techniques":["small angle scattering"]})
> print(matches)
[{'inText': 'small angle scattering', 'inPaNET': {'technique': {'id': 'http://purl.org/pan-science/PaNET/PaNET01124', 'label': 'small angle scattering', 'altLabel': ['SAS', 'small angle diffraction'], 'subClassOf': {'PaNET01037': 'low momentum transfer scattering'}, 'definition1': '', 'definition2': 'https://en.wikipedia.org/wiki/Small-angle_scattering'}, 'score': 0.0}}]
```
