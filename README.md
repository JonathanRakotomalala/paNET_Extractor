# PaNET terms extraction 

Points out technics from scientific text and maps them into the PaNET ontology terms with all details.

## Setting up environment
Use [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)  to create the virtual environemnt and [pip](https://pip.pypa.io/en/stable/) to install.

## Project structure
In the src there are 7 modules:
levenshtein: levenshtein distance of the strings
llm: string extraction from text
matchmapper: match the techniques with terms
ontology: import paNET ontology
openaire: import abstract from doi
orchestrator: orchestrate all the operations for techniques extraction
service_evaluation: evaluate the service with a list of dois

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.