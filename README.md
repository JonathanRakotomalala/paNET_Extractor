# PaNET term extraction 

Points out techniques from scientific texts and maps them into the PaNET ontology terms with all details.


## Setting up environment

Use [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to create the virtual environment
and [pip](https://pip.pypa.io/en/stable/) to install new packages.

Execute `uv sync` to install all dependencies defined in the project. <br>
3 environment variables are required:
- OPEN_AIRE_REFRESH_ACCESS_TOKEN
- ACCESS_TOKEN
- USER_AGENT_MAIL
## Project structure

> In the `packages` directory there are 3 packages:
1. `panet-technique-matcher`: calculate the distance between strings with rapidfuzz
2. `ontology`: import paNET ontology

2. `technique-extractor`: string extraction from text
3. `data-provider`: import abstract from DOIs using OpenAire API

> In the `src`:
1. `panetextractor`: 
    1. `api`: the endpoints and the api ddocs settings
    2. `orchestrator`: orchestrate all the operations for techniques extraction
2. `service_evaluation`: a script to evaluate the service with a list (length=3) of random DOIs


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

