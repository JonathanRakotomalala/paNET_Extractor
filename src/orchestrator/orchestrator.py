from src.llm.llm import Llm
from src.matchmapper.matchmapper import MatchMapper
import json
from fastapi import HTTPException
from ..ontology.ontology_import import EmptyOntologyError
from ..openaire import OpenAire, AbstractImportError,RateLimitError


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
    
    def list_search(doi_list):
        try :
            my_list=[]
            for _,i in doi_list:
                for j in i:
                    abstract = OpenAire.get_abstract_from_doi(j)
                    techniques = Orchestrator.search(abstract)
                    my_list.append({"doi":j,"abstract":abstract,"techniques":techniques})
            return {"outputs":my_list}
        except (AbstractImportError,RateLimitError) as e:
            if isinstance(e,AbstractImportError):
                raise HTTPException(status_code=404,detail=e.message,headers={"message": e.message})
            else:
                raise HTTPException(status_code=429,detail={"error":"too many requests"},headers={"Retry-After":e.retry})
        
