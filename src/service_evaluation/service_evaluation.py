
import math
from src.openaire import OpenAire
import httpx
import asyncio
import json


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
                page = await httpx.AsyncClient().get("https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025,keywords.id:keywords/crystal,primary_topic.id:t10247" + "&page=" + str(i+1))
                await httpx.AsyncClient().aclose()
                if page.status_code == 200:

                    for j in page.json()["results"]:
                        print(j["doi"])
                        if j["doi"] is not None:
                            my_doi_list.append(j["doi"].split("https://doi.org/")[-1])

            print(my_doi_list)
            response = await httpx.AsyncClient().post(
                url="http://127.0.0.1:8000/dois_to_techniques/",
                headers={
                    "Authorization": "Bearer "+OpenAire.TOKEN,
                    "User-Agent": "PaNetExtractor/1.0.0 (jonathan.rakotomalala@esrf.fr)",
                    "Content-type": "application/json",
                    "Accept": "application/json",
                },
                json={"dois": my_doi_list},
                timeout=None
            )
            await httpx.AsyncClient().aclose()
            if response.status_code == 200:
                with open("data/results.json", "w") as file:
                    file.write(json.dumps(response.json()))
            else :
                print(response.status_code)
                print(response.json())


async def main():
    await ServiceEvaluation.evaluate_service()

if __name__ == "__main__":
    asyncio.run(main())