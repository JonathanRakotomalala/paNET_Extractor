from src.llm.llm import Llm
from src.matchmapper.matchmapper import MatchMapper
import json
from fastapi import HTTPException
from ..ontology.ontology_import import EmptyOntologyError

class Orchestrator:
    def search(input: str):
        extracted_techniques = Llm.llm_run(input)
        try:
            data = json.loads(extracted_techniques)
            return {"output": MatchMapper.map_to_panet(data)}
        except (json.JSONDecodeError,EmptyOntologyError) as e:
            if isinstance(e,EmptyOntologyError):
                raise HTTPException(status_code=404,detail=e.message,headers={"message": e.message})
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request",
                    headers={"message": "Bad Request"},
                )
