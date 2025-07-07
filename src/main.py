from .orchestrator.orchestrator import Orchestrator
from fastapi import FastAPI, Query, Request
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi


class TechniqueDetails(BaseModel):
    label: str
    altLabel: list[str]
    subClassOf: dict
    definition1: str
    definition2: str


class Technique(BaseModel):
    technique: TechniqueDetails


class TextTechnique(BaseModel):
    inText: str
    inPaNET: Technique


class Result(BaseModel):
    output: list[TextTechnique] = Field(
        examples=[
            {
                "inText": "Small-angle scattering",
                "InPaNET": {
                    "technique": {
                        "label": "high resolution inelastic neutron scattering",
                        "altLabel": [],
                        "subClassOf": {
                            "PaNET01042": "high energy resolution emission technique",
                            "PaNET01245": "inelastic neutron spectroscopy",
                        },
                    }
                },
            }
        ]
    )


class Message(BaseModel):
    detail: str = Field(examples=["Error while trying to load ontology"])


app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/doc_elem", include_in_schema=False)
async def api_documentation(request: Request):
    return HTMLResponse("""<!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Elements in HTML</title>

        <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
    </head>
    <body>

        <elements-api
        apiDescriptionUrl="openapi.json"
        router="hash"
        />

    </body>
    </html>""")


@app.post("/techniques/", responses={200: {"model": Result}, 400: {"descripton": "Bad Request"}, 404:{"model":Message}})
def get_techniques(
    input: Annotated[str, Query(max_length=2500, min_length=2)],
) -> Result:
    """Get techniques from the text"""
    return Orchestrator.search(input)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="PaNetExtractor",
        version="0.1.0",
        summary="Extract techniques from a text",
        description="Using an LLM it searches for techniques then maps the techniques found with the techniques from the PaNET ontology",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
