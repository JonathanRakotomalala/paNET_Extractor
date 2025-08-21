import time
import os
import requests
from dotenv import find_dotenv, load_dotenv

# find the .env then load the environment secrets and variables
load_dotenv(find_dotenv())


class AbstractImportError(Exception):
    def __init__(self, message="OpenAire Error"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class RateLimitError(Exception):
    def __init__(self, retry, message="OpenAire Error"):
        self.retry = retry
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message + self.retry}"


class DataProvider:
    """
    Manages the authentication and interactions with OpenAire search products API

    Attributes:
        openaire_token : A str used for authenticating API requests.
        user_agent_mail : A str that represent the user's email
    """

    openaire_token = None
    USER_AGENT_MAIL = os.getenv("USER_AGENT_MAIL")

    def __init__(self):
        # OPEN_AIRE_REFRESH_ACCESS_TOKEN is a token that permits to get an hour token for authenticated request to have 7200 requests/h
        # instead of  60 requests/h (https://graph.openaire.eu/docs/apis/terms) : https://graph.openaire.eu/docs/apis/authentication#personal-access-token
        OPEN_AIRE_REFRESH_ACCESS_TOKEN = os.getenv("OPEN_AIRE_REFRESH_ACCESS_TOKEN")
        response_token = requests.get(
            "https://services.openaire.eu/uoa-user-management/api/users/getAccessToken?refreshToken="
            + OPEN_AIRE_REFRESH_ACCESS_TOKEN
        )

        if response_token.status_code == 200:
            DataProvider.openaire_token = response_token.json()["access_token"]
        else:
            raise AbstractImportError("Invalid OpenAire Access Token")

    def get_registry_agency(doi: str):
        url_link = "https://doi.org/doiRA/" + doi
        response = requests.get(url_link)
        if response.status_code == 200 and "RA" in response.json()[0]:
            return response.json()[0]["RA"]
        else:
            raise AbstractImportError("Error with the doiRA API")

    def call_datacite(doi):
        url_link = "https://datacite.org/dois?query=doi:" + doi
        response = requests.get(url_link)
        if response.status_code == 200:
            return response.json()
        else:
            raise AbstractImportError("Error with the Datacite API")

    def call_open_aire(doi):
        """
        calls OpenAire search products API to get informations from the doi

        Args:
            doi: a string that represent a DOI
        Return:
            a Response

        Raises:
            RateLimitError: If the requests limit of openaire api is reached
            AbstractImportError: If failed to get a good response
        """
        url_link = "https://api.openaire.eu/graph/v1/researchProducts?pid=" + doi

        response = requests.get(
            url_link,
            headers={
                "Authorization": "Bearer " + DataProvider.openaire_token,
                "User-Agent": "PaNetExtractor/1.0.0 ("
                + DataProvider.USER_AGENT_MAIL
                + ")",
            },
        )
        time_start = time.time()

        if response.status_code == 200 and response.json()["header"]["numFound"] > 0:
            return response
        elif response.status_code == 429:
            if "Retry-After" not in response.headers:
                # waiting time  = difference of the time of the request and the time of the request rounded to the upper hour
                waiting_time = (time_start + 3600) - time_start
            else:
                waiting_time = int(response.headers["Retry-After"])
            raise RateLimitError(waiting_time, "Too many requests")
        else:
            print(response.status_code)
            raise AbstractImportError("Unable to extract abstract from DOI")

    def get_abstract_from_doi(doi):
        """
        gets the abstract with openaire's api

        Args:
            doi: a string that represent the digital object identifier

        Returns:
            A string, the abstract of the publication

        Raise:
            RateLimitError: If the requests limit of openaire api is reached
            AbstractImportError: If failed to get the abstract

        """
        try:
            abstract = "No abstract available"
            registry = DataProvider.get_registry_agency(doi)
            print(registry)
            if registry == "Crossref":
                response = DataProvider.call_open_aire(doi)
                json_response = response.json()
                results = json_response.get("results", [])
                if (
                    results
                    and "descriptions" in results[0]
                    and results[0]["descriptions"]
                ):
                    abstract = results[0]["descriptions"][0]
            elif registry == "DataCite":
                response = DataProvider.call_datacite(doi)

                datas = response.get("data", [])
                if (
                    datas
                    and "descriptions" in datas[0]["attributes"]
                    and datas[0]["attributes"]["descriptions"]
                ):
                    abstract = datas[0]["attributes"]["descriptions"][0]["description"]
        except (AbstractImportError, RateLimitError) as e:
            if isinstance(e, AbstractImportError):
                abstract = "Error: No abstract available"
            else:
                raise RateLimitError(e.retry, "Too many requests")

        return abstract
