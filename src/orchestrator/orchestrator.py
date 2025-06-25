from src.llm.llm import Llm
from src.matchmapper.matchmapper import MatchMapper
import json




class Orchestrator:
    
    def search(input:str):
        extracted_techniques=Llm.llm_run(input)
        try:
          data = json.loads(extracted_techniques)
          return {"output":MatchMapper.map_to_panet(data)}
        except json.JSONDecodeError:
            return {"output":[]}

        
