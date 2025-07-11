
import math
from src.openaire import OpenAire
import httpx
import requests 


LINK = "https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025 "
LENGTH = len("https://doi.org/")


class ServiceEvaluation:
    
    async def evaluate_service():
        """Evaluate the service that extracts technics from the dois of publication from the year 2025"""

        response = await httpx.AsyncClient().get(
            "https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025,keywords.id:keywords/crystal,primary_topic.id:t10247",
        )
        if response.status_code == 200:
            meta = response.json()["meta"]
            nb_page = math.ceil(meta["count"] / meta["per_page"])
            my_doi_list = []
            for i in range(0, nb_page):
                print(nb_page)
                page = await httpx.AsyncClient().get(LINK + "&page=" + str(i+1))
                if page.status_code == 200:

                    for j in page.json()["results"]:
                        print(j["doi"])
                        if j["doi"] is not None:
                            my_doi_list.append(j["doi"].split("https://doi.org/")[-1])
            print(my_doi_list)
            response = requests.post(
                url="http://127.0.0.1:8000/dois_to_techniques/",
                headers={
                    "Authorization": "Bearer "+OpenAire.TOKEN,
                    "User-Agent": "PaNetExtractor/1.0.0 (jonathan.rakotomalala@esrf.fr)",
                    "Content-type": "application/json",
                    "Accept": "application/json",
                },
                json={"dois": my_doi_list},
            )

            if response.status_code == 200:
                with open("../../data/results.json", "w") as file:
                    file.write(response.json())
            else :
                print(response.status_code)
                print(response.json())
