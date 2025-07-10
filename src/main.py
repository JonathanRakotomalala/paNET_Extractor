from .orchestrator.orchestrator import Orchestrator
from fastapi import FastAPI, Query, Request,Body,HTTPException
from fastapi.responses import JSONResponse
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

class BadRequestMessage(BaseModel):
    detail: str = Field(examples=["Bad request"])

class CannotAcceptMesssage(BaseModel):
    detail: str = Field(examples=["Not acceoted must be an application/json"])

class RateLimitMessage(BaseModel):
    detail: str = Field(examples=["Too many requests"])

class Dois(BaseModel):
    dois:list[str]

class DoiTechResponse(BaseModel):
    doi:str
    abstract:str 
    techniques:Result

class DoiTechResponses(BaseModel):
    outputs:list[DoiTechResponse]

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


@app.post("/extract_techniques/", responses={200: {"model": Result}, 400: {"descripton": "Bad Request","model":BadRequestMessage}, 404:{"model":Message},406:{"model":CannotAcceptMesssage}},response_class=JSONResponse)
def get_techniques(request: Request,
    input: Annotated[str, Query(max_length=2500, min_length=2,example='NiFe-layered double hydroxides (LDHs) are promising electrocatalysts for the oxygen evolution reaction (OER) in alkaline media. Here, operando X-ray diffraction (XRD) and X-ray total scattering are used with Pair Distribution Function (PDF) analysis to investigate the atomic structure of the catalytically active material and follow structural changes under operating conditions. XRD shows an interlayer contraction under applied oxidative potential, which relates to a transition from the α-LDH to the γ-LDH phase. The phase transition is reversible, and the α-LDH structure is recovered at 1.3 VRHE. However, PDF analysis shows an irreversible increase in the stacking disorder under operating conditions, along with a decrease in the LDH sheet size. The analysis thus shows that the operating conditions induce a breakdown of the particles leading to a decrease in crystallite size.') ],
) -> Result:
    """Get techniques from raw text"""
    if "application/json" not in request.headers.get("accept",""):
        raise HTTPException(status_code=406,detail = "Not accepted must be an application/json")
    else:
        return Orchestrator.search(input)

@app.post("/dois_to_techniques/",responses={404:{"model":Message},406:{"model":CannotAcceptMesssage},429:{}},response_class=JSONResponse)
def get_techniques_from_dois(request:Request,dois:Annotated[Dois,Body(example = {"dois":["10.1007/s00396-004-1145-9","10.1002/smll.202411211","10.3406/bspf.2011.14065"]})])->DoiTechResponses:
    """Get techniques from DOIs"""
    if "application/json" not in request.headers.get("accept",""):
        raise HTTPException(status_code=406,detail = "Not accepted must be an application/json")
    else:
        return Orchestrator.list_search(dois)


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

if __name__ == "__main__":
    Orchestrator.evaluate()