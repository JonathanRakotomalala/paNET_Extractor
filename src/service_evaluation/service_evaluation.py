
import math
from src.openaire import OpenAire
import httpx
import asyncio
import json
import random

LINK = "https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025 "
LENGTH = len("https://doi.org/")


class ServiceEvaluation:
    
    async def evaluate_service():
        """Evaluate the service that extracts technics from the dois of publication from the year 2025"""
        client = httpx.AsyncClient()

        response = await client.get(
            "https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025",
        )
        if response.status_code == 200:

            meta = response.json()["meta"]
            nb_page = math.ceil(meta["count"] / meta["per_page"])
            def index_is_equal(x):
                return x.index in [random.range(0,nb_page),random.range(0,nb_page),random.range(0,nb_page)]
            my_doi_list = []

            # for i in range(0, nb_page):
            #     print(nb_page)
            #     page = await client.get("https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025,keywords.id:keywords/crystal,primary_topic.id:t10247" + "&page=" + str(i+1))
            #     if page.status_code == 200:

            #         for j in page.json()["results"]:
            #             print(j["doi"])
            #             if j["doi"] is not None:
            #                 my_doi_list.append(j["doi"].split("https://doi.org/")[-1])

            requests = []
            print(nb_page)
            for i in range(1, nb_page + 1):
                
                requests.append(client.get("https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025" + "&page=" + str(i)))
            
            # wait all the parallel responses
            try:
                responses = await asyncio.gather(*requests)
            except httpx.RequestError as e:
                print(f"Erreur lors de la récupération des pages: {e}")
                return
            


            for page_response in responses:
                if page_response.status_code == 200:
                    for j in page_response.json()["results"]:
                        if j.get("doi"):
                            my_doi_list.append(j["doi"].split("https://doi.org/")[-1])

            print(my_doi_list)

            sample_dois = random.sample(my_doi_list, min(3, len(my_doi_list)))
            print(f"3 selected : {sample_dois}")

            response = await client.post(
                url="http://127.0.0.1:8000/dois_to_techniques/",
                headers={
                    "Authorization": "Bearer "+OpenAire.TOKEN,
                    "User-Agent": "PaNetExtractor/1.0.0 (jonathan.rakotomalala@esrf.fr)",
                    "Content-type": "application/json",
                    "Accept": "application/json",
                },
                json={"dois": sample_dois},
                timeout=None
            )
            
            if response.status_code == 200:
                with open("data/results.json", "w") as file:
                    file.write(json.dumps(response.json()))
            else :
                print(response.status_code)
                print(response.json())
            await client.aclose()


async def main():
    await ServiceEvaluation.evaluate_service()

if __name__ == "__main__":
    asyncio.run(main())