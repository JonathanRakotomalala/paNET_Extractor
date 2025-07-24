
import random
import math
import httpx
import asyncio
import json
from fastapi.testclient import TestClient
from src.main import app

LINK = "https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025"
LENGTH = len("https://doi.org/")


class ServiceEvaluation:
    """
        Evaluates the services by using it on samples
    """
    async def evaluate_service():
        """Evaluate the service that extracts technics from the dois of publication from the year 2025 (from openalex api)"""
        # to make asynchronous operations
        client = httpx.AsyncClient()

        response = await client.get(
            LINK,
        )
        if response.status_code == 200:

            meta = response.json()["meta"]
            nb_page = math.ceil(meta["count"] / meta["per_page"]) #calculate the total number of page 
            my_doi_list = []

            open_alex_requests = []
            print(nb_page)
            #iterate on the pages
            for i in range(1, nb_page + 1):
                
                open_alex_requests.append(client.get(LINK + "&page=" + str(i)))
            # wait for alle the requests to end
            responses = await asyncio.gather(*open_alex_requests)


            # treat all answers => get all dois and pass onto the next if no doi
            for page_response in responses:
                if page_response.status_code == 200:
                    for j in page_response.json()["results"]:
                        if j.get("doi"):
                            my_doi_list.append(j["doi"].split("https://doi.org/")[-1])

            print(my_doi_list)

            # pick 3 random dois
            sample_dois = random.sample(my_doi_list, min(4, len(my_doi_list)))
            print(f"3 selected : {sample_dois}")
            # retrieve the token for openaire authentication
            # OpenAire()
            # make a request to our service
            with TestClient(app) as appclient:
                response = appclient.post(
                    url="http://127.0.0.1:8000/dois_to_techniques/",
                    headers={
                        "Content-type": "application/json",
                        "Accept": "application/json",
                    },
                    json={"dois": sample_dois},
                    timeout=None
                )
                if response.status_code == 200:
                    with open("tests/data/results.json", "w") as file:
                        file.write(json.dumps(response.json()))
                else :
                    print(f"Erreur HTTP {response.status_code}: {response.text}")
                    print(response.status_code)
                    print(response.json())
            await client.aclose()
        




async def main():
    await ServiceEvaluation.evaluate_service()

if __name__ == "__main__":
    asyncio.run(main())
