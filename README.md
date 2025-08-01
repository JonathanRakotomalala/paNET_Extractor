# PaNET term extraction 

Points out techniques from scientific texts and maps them into the PaNET ontology terms with all details.


## Setting up environment

Use [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to create the virtual environment
and [pip](https://pip.pypa.io/en/stable/) to install new packages.

Execute `uv sync` to install all dependencies defined in the project.


## Project structure

In the `src` directory there are 7 packages:
1. `scorerapidfuzz`: calculate the distance between strings with rapidfuzz
2. `llm`: string extraction from text
3. `matchmapper`: match the techniques with terms
4. `ontology`: import paNET ontology
5. `openaire`: import abstract from DOIs using OpenAire API
6. `orchestrator`: orchestrate all the operations for techniques extraction
7. `service_evaluation`: a script to evaluate the service with a list of random DOIs


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
