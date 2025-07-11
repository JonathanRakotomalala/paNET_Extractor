from ..llm.llm import Llm
from ..matchmapper.matchmapper import MatchMapper
import json
from fastapi import HTTPException
from ..ontology.ontology_import import EmptyOntologyError
from ..openaire import OpenAire, AbstractImportError, RateLimitError
import time
import math


class Orchestrator:
    time_start = None
    
    def search(input: str):
        """
            Search the techniques in the text and map them to those in paNET

            Args:
                input: a string
            
            Returns:
                the techniques and it best matching term from paNET

            Raises:
                HTPPException: if failed to get the techniques from the text or failed to import ontology 
        """
        extracted_techniques = Llm.llm_run(input)
        try:
            data = json.loads(extracted_techniques)
            return {"output": MatchMapper.map_to_panet(data)}
        except (json.JSONDecodeError, EmptyOntologyError) as e:
            if isinstance(e, EmptyOntologyError):
                raise HTTPException(
                    status_code=404, detail=e.message, headers={"message": e.message}
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request",
                    headers={"message": "Bad Request"},
                )

    def list_search(doi_list):
        """
            Get the doi's abstract and search teh techniques

            Args:
                doi_list: a list of str 

            Returns:
                the dois, their corresponding abstract and the techniques found
            
            Raises:
                HTTPException: If failed to get the abstract or reached request rate limit
        """
        try:
            print(Orchestrator.time_start)
            if Orchestrator.time_start is None or Orchestrator.time_start<=time.time():
                my_list = []
                for _, i in doi_list:
                    for j in i:
                        abstract = OpenAire.get_abstract_from_doi(j)
                        techniques = Orchestrator.search(abstract)
                        my_list.append(
                            {"doi": j, "abstract": abstract, "techniques": techniques}
                        )
                return {"outputs": my_list}
            else:
                raise RateLimitError(str(math.ceil(Orchestrator.time_start-time.time())))
        except (AbstractImportError, RateLimitError) as e:
            if isinstance(e, AbstractImportError):
                raise HTTPException(
                    status_code=404, detail=e.message, headers={"message": e.message}
                )
            else:
                Orchestrator.time_start = time.time()+float(e.retry)
                raise HTTPException(
                    status_code=429,
                    detail={"error": e.message},
                    headers={"Retry-After": str(e.retry)},
                )

