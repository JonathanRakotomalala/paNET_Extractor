from .orchestrator.orchestrator import Orchestrator
from fastapi import FastAPI, Query, Request,Body,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from typing import List


class TechniqueDetails(BaseModel):
    id: str = Field(examples=["http://purl.org/pan-science/PaNET/PaNET01320"])
    label: str = Field(examples=["fourier transform infrared spectroscopy"])
    altLabel: list[str] = Field(examples=[["FTIR"]])
    subClassOf: dict = Field(examples=[{"PaNET00209": "interferometry technique",
                                    "PaNET01109": "infrared spectroscopy"}])
    definition1: str = Field(examples=[""])
    definition2: str = Field(examples=["https://en.wikipedia.org/wiki/Fourier-transform_infrared_spectroscopy"])

class Technique(BaseModel):
    technique: TechniqueDetails
    score:float

class TextTechnique(BaseModel):
    inText: str = Field(examples=["FTIR"])
    inPaNET: Technique


class Result(BaseModel):
    output: List[TextTechnique] 


class Message(BaseModel):
    detail: str = Field(examples=["Error while trying to load ontology:ontology not found"])

class BadRequestMessage(BaseModel):
    detail: str = Field(examples=["Bad request"])

class CannotAcceptMesssage(BaseModel):
    detail: str = Field(examples=["Not accepted must be an application/json"])

class RateLimitMessage(BaseModel):
    detail: str = Field(examples=["Too many requests"])

class Dois(BaseModel):
    dois:list[str]

class DoiTechResponse(BaseModel):
    doi:str = Field(examples=["10.1073/pnas.2411406122"])
    abstract:str = Field(examples = ["<jats:p>             Heterogeneous catalysts have emerged as a potential key for closing the carbon cycle by converting carbon dioxide (CO             <jats:sub>2</jats:sub>             ) into value-added chemicals. In this work, we report a highly active and stable ceria (CeO             <jats:sub>2</jats:sub>             )-based electronically tuned trimetallic catalyst for CO             <jats:sub>2</jats:sub>             to CO conversion. A unique distribution of electron density between the defective ceria support and the trimetallic nanoparticles (of Ni, Cu, Zn) was established by creating the strong metal support interaction (SMSI) between them. The catalyst showed CO productivity of 49,279 mmol g             <jats:sup>\u22121</jats:sup>             h             <jats:sup>\u22121</jats:sup>             at 650 \u00b0C. CO selectivity up to 99% and excellent stability (rate remained unchanged even after 100 h) stemmed from the synergistic interactions among Ni-Cu-Zn sites and their SMSI with the defective ceria support. High-energy-resolution fluorescence-detection X-ray absorption spectroscopy (HERFD-XAS) confirmed this SMSI, further corroborated by in situ electron energy loss spectroscopy (EELS) and density functional theory (DFT) simulations. The in situ studies (HERFD-XAS &amp; EELS) indicated the key role of oxygen vacancies of defective CeO             <jats:sub>2</jats:sub>             during catalysis. The in situ transmission electron microscopy (TEM) imaging under catalytic conditions visualized the movement and growth of active trimetallic sites, which completely stopped once SMSI was established. In situ FTIR (supported by DFT) provided a molecular-level understanding of the formation of various reaction intermediates and their conversion into products, which followed a complex coupling of direct dissociation and redox pathway assisted by hydrogen, simultaneously on different active sites. Thus, sophisticated manipulation of electronic properties of trimetallic sites and defect dynamics significantly enhanced catalytic performance during CO             <jats:sub>2</jats:sub>             to CO conversion.           </jats:p>"])
    techniques:list[TextTechnique]|str

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

@app.post("/dois_to_techniques/",responses={404:{"model":Message},406:{"model":CannotAcceptMesssage},429:{"model":RateLimitMessage}},response_class=JSONResponse)
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


