import requests
from src.openaire import OpenAire

LINK = "https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025 "
LENGTH = len("https://doi.org/")


class ServiceEvaluation:
    def evaluate_service():
        """Evaluate the service that extracts technics from the dois of publication from the year 2025"""

        response = requests.get(
            "https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025",
            headers={
                "Authorization": "Bearer "+ OpenAire.TOKEN,
                "User-Agent": "PaNetExtractor/1.0.0 (jonathan.rakotomalala@esrf.fr)",
            },
        )
        if response.status_code == 200:
            meta = response.json()["meta"]
            nb_page = round(meta["count"] / meta["per_page"])

            for i in range(1, nb_page):
                page = requests.get(LINK + "&page=" + str(i))
                if page.status_code == 200:
                    my_doi_list = []
                    for j in page.json()["results"]:
                        print(j["doi"])
                        if j["doi"] is not None:
                            my_doi_list.append(j["doi"][-LENGTH])
            response = requests.post(
                url="http://127.0.0.1:8000/dois_to_techniques/",
                headers={
                    "Authorization": "Bearer "+OpenAire.TOKEN,
                    "User-Agent": "PaNetExtractor/1.0.0 (jonathan.rakotomalala@esrf.fr)",
                    "Content-type": "application/json",
                    "Accept": "application/json",
                },
                data={"dois": my_doi_list},
            )
            if response.status_code == 200:
                with open("../results.json", "w") as file:
                    file.write(response.json())
