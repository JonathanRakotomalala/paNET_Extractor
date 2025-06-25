from src.llm.llm import QUERY_1
from .orchestrator.orchestrator import Orchestrator
from fastapi import FastAPI,Query
from pydantic import BaseModel
from fastapi import HTTPException
from typing_extensions import Annotated



app = FastAPI()

class TechniqueDetails(BaseModel):
    label:str
    altLabel: list[str]
    subClassOf: dict
    definition1: str 
    definition2: str

class Technique(BaseModel):
    technique:TechniqueDetails

class TextTechnique(BaseModel):
    inText:str
    inPaNET:Technique

class Result(BaseModel):
    output:list[TextTechnique]|list



@app.post("/techniques/")
def get_techniques(input:Annotated[str,Query(max_length=500,min_length=2)]) ->Result:
    return Orchestrator.search(input)
if __name__ == "__main__":
    Orchestrator.search(QUERY_1)