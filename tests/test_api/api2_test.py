import requests
from fastapi.testclient import TestClient
from src.main import app


LINK = " https://api.openalex.org/works?filter=authorships.institutions.lineage:i2801997478,publication_year:2025"
LENGTH = len("https://doi.org/")

response = requests.get(LINK)

if response.status_code == 200:
    meta = response.json()["meta"]
    results = response.json()["results"]

    nb_page = round(meta["count"] / meta["per_page"])

    for i in range(2, nb_page + 1):
        page = requests.get(LINK + "&page=" + i)
        if page.status_code == 200:
            my_doi_list = []
            for j in page.json()["results"]:
                my_doi_list.append(j["doi"][-LENGTH])

    with TestClient(app) as client:
        response = client.post(
            url="http://127.0.0.1:8000/dois_to_techniques/",
            headers={"Content-type": "application/json", "Accept": "application/json"},
            data={'dois':my_doi_list}
        )
        if response.status_code==200:
            print(response.json())
