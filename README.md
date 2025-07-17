# PaNET terms extraction 

Points out technics from scientific text and maps them into the PaNET ontology terms with all details.

## Setting up environment
Use [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)  to create the virtual environemnt and [pip](https://pip.pypa.io/en/stable/) to install new packages if needed.</br>
uv sync to install all dependencies defined in the project.

## Project structure
In the src there are 7 modules:</br>
1. levenshtein: levenshtein distance of the strings</br>
2. llm: string extraction from text</br>
3. matchmapper: match the techniques with terms</br>
4. ontology: import paNET ontology</br>
5. openaire: import abstract from doi</br>
6. orchestrator: orchestrate all the operations for techniques extraction</br>
7. service_evaluation: a script to evaluate the service with a list of random dois</br>

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
