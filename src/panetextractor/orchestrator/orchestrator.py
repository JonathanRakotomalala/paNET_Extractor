from src.panetextractor import MatchMapper, Llm, DataProvider
from fastapi import HTTPException
from packages.panet_technique_matcher.src.panet_technique_matcher.ontology_importer import (
    EmptyOntologyError,
    OntologyNotFoundError,
)
from packages.data_provider.src.data_provider import RateLimitError
import time
import math
import json


class Orchestrator:
    """
    Orchestrates the operations for techniques extraction

    Attributes:
        time_start: A float that represent the time at which the user cans start requests, default to None
        llm_instance: Instance of the Llm class
    """

    time_start = None  # The time at which the user can restart to make a requests, None if error 429 has'nt occured yet
    DataProvider()  # initialize openaire

    llm_instance = Llm()

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

        extracted_techniques = Orchestrator.llm_instance.llm_run(input)
        try:
            data = json.loads(extracted_techniques)
            return {
                "algorithm": "Levenshtein's distance",
                "output": MatchMapper.map_to_panet(data),
            }
        except (json.JSONDecodeError, EmptyOntologyError, OntologyNotFoundError) as e:
            if isinstance(e, EmptyOntologyError) or isinstance(
                e, OntologyNotFoundError
            ):
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
        Gets the doi's abstract and search teh techniques

        Args:
            doi_list: a list of str

        Returns:
            the dois, their corresponding abstract and the techniques found

        Raises:
            HTTPException: If failed to get the abstract or reached request rate limit
        """
        try:
            # if time_start is past we can call openaire and do the operations

            if (
                Orchestrator.time_start is None
                or Orchestrator.time_start <= time.time()
            ):
                my_list = []
                for _, i in doi_list:
                    for j in i:
                        result = DataProvider.get_abstract_from_doi(j)
                        # first_result = OpenAire.get_abstract_from_doi(j)
                        # result = re.sub(r'<.*?>', ' ',first_result )
                        if result == "No abstract available":
                            techniques = []
                        else:
                            try:
                                techniques = Orchestrator.search(result)["output"]
                            except HTTPException:
                                techniques = (
                                    "Error could not extract and map techniques"
                                )

                        my_list.append(
                            {"doi": j, "abstract": result, "techniques": techniques}
                        )

                return {"algorithm": "Levenshtein's distance", "outputs": my_list}
            # else we calculate the remaining time until we can make a request and we raise an exception
            else:
                raise RateLimitError(
                    str(math.ceil(Orchestrator.time_start - time.time()))
                )
        except RateLimitError as e:
            # # 429 error we set time_start to the actual time plus the retry-after
            Orchestrator.time_start = time.time() + float(e.retry)
            raise HTTPException(
                status_code=429,
                detail={"error": e.message},
                headers={"Retry-After": str(e.retry)},
            )
