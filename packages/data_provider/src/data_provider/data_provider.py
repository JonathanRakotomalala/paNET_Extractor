import time
import os
import requests
from dotenv import find_dotenv, load_dotenv
import logging

logger = logging.getLogger(__name__)

# find the .env then load the environment secrets and variables
load_dotenv(find_dotenv())


class AbstractImportError(Exception):
    def __init__(self, message="OpenAire Error"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class NoPublicationFoundError(Exception):
    def __init__(self, message="publication not found"):
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
    Manages the authentication and interactions with OpenAire search products and Datacite API

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
        """The registry agency of the publication
        Args:
            doi
        Returns:
            The registry agency
        Raises :
            AbstractImportError
        """
        url_link = "https://doi.org/doiRA/" + doi.replace(",", "%2C")
        response = requests.get(url_link)
        if response.status_code != 200:
            raise AbstractImportError(f"Http Error response {response.status_code}")
        if "RA" not in response.json()[0]:
            raise AbstractImportError(f"Error : {response.json()[0]['status']}")
        return response.json()[0]["RA"]

    def call_datacite(doi):
        """
        get informations from the doi
        Args: doi
        Returns:
        Raises: AbstractImportError
        """
        url_link = "https://datacite.org/dois?query=doi:" + doi
        response = requests.get(url_link)
        match response.status_code:
            case 200:
                if len(response.json()["data"]) > 0:
                    return response.json()
                raise NoPublicationFoundError("DataCite did not find the publication")
            case _:
                raise AbstractImportError(
                    f"Error DataCite: Http Error response {response.status_code}"
                )

    def call_open_aire(doi):
        """
        calls OpenAire search products API to get informations from the doi

        Args:
            doi: a string that represent a DOI
        Returns:
            a Response

        Raises:
            RateLimitError: If the requests limit of openaire api is reached
            AbstractImportError: If failed to get a good response
        """
        url_link = "https://api.openaire.eu/graph/v1/researchProducts?pid=" + doi

        response = requests.get(
            url_link,
            headers={
                "Authorization": f"Bearer {DataProvider.openaire_token}",
                "User-Agent": f"PaNetExtractor/1.0.0 ({DataProvider.USER_AGENT_MAIL})",
            },
        )

        logger.debug(response.json())
        match response.status_code:
            case 200:
                if response.json()["header"]["numFound"] > 0:
                    return response
                else:
                    raise NoPublicationFoundError("OpenAire did not find publication")
            case 429:
                if "Retry-After" not in response.headers:
                    # waiting time  = difference of the time of the request and the time of the request rounded to the upper hour
                    waiting_time = 3600
                else:
                    waiting_time = int(response.headers["Retry-After"])
                raise RateLimitError(waiting_time, "Too many requests")
            case _:
                print(response.status_code)
                raise AbstractImportError(
                    f"Unable to extract abstract from DOI due to openaire: Http error {response.status_code}"
                )

    def get_abstract_from_doi(doi: str):
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
            registry = DataProvider.get_registry_agency(doi)
            logger.info(registry)
            match registry:
                case "Crossref":
                    response = DataProvider.call_open_aire(doi)
                    json_response = response.json()
                    results = json_response.get("results", [])
                    if (
                        results
                        and "descriptions" in results[0]
                        and results[0]["descriptions"]
                    ):
                        return results[0]["descriptions"][0]
                case "DataCite":
                    response = DataProvider.call_datacite(doi)

                    datas = response.get("data", [])
                    if (
                        datas
                        and "descriptions" in datas[0]["attributes"]
                        and datas[0]["attributes"]["descriptions"]
                    ):
                        return datas[0]["attributes"]["descriptions"][0]["description"]
        except (AbstractImportError, RateLimitError) as e:
            if isinstance(e, AbstractImportError):
                logger.error(e)
                return f"Error: Could not get the abstract due to {e}"
            else:
                raise RateLimitError(e.retry, "Too many requests")

        return "No abstract available"
