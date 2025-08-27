# PaNET term extraction 

Points out techniques from scientific texts and maps them into the PaNET ontology terms with all details.


## Setting up environment

Use [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) to create the virtual environment
and [pip](https://pip.pypa.io/en/stable/) to install new packages.

Execute `uv sync` to install all dependencies defined in the project. <br>
3 environment variables are required:
- HUGGING_FACE_ACCESS_TOKEN: Huggingface access token (more info here)
- OPEN_AIRE_REFRESH_ACCESS_TOKEN: OpenAire refresh access token (more info here)
- USER_AGENT_MAIL: An e-mail (more info here)

### Docker 
There is a dockerfile to build a docker image of the project : 

To build and run a container : 
```console
> docker build -t name_of_image path_to_the_build_context 
> docker run -p 8000:80 id_or_name_of_image
```
API docs at https://localhost:8000/doc_elem#

## Project structure

> In the `packages` directory there are 3 packages:
1. <a href="packages\panet_technique_matcher\README.md">`panet-technique-matcher`</a>>: tools for matchmapping of the techniques
2.  <a href="packages\techniques_extractor\README.md">`techniques-extractor`</a>: technique extraction from text
3.  <a href="packages\data_provider\README.md">`data-provider`</a>: import abstract from DOIs using OpenAire API

> In the `src`:
1. `panetextractor`: 
    1. `api`: the endpoints and the api docs settings
    2. `orchestrator`: orchestrate all the operations for techniques extraction
2. `service_evaluation`: a script to evaluate the service with a list (length=3) of random DOIs. Results<a href="\tests\data\results.json"> here</a>


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

