import time
import os
import requests


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


class OpenAire:
    """
    Manages the authentication and interactions with OpenAire search products API

    Attributes:
        _openaire_token : A str used for authenticating API requests.
        user_agent_mail : A str that represent the user's email
    """

    _openaire_token = None
    _USER_AGENT_MAIL = os.getenv("USER_AGENT_MAIL")

    def __init__(self):
        # OPEN_AIRE_REFRESH_ACCESS_TOKEN is a token that permits to get an hour token for authenticated request to have 7200 requests/h
        # instead of  60 requests/h (https://graph.openaire.eu/docs/apis/terms) : https://graph.openaire.eu/docs/apis/authentication#personal-access-token
        OPEN_AIRE_REFRESH_ACCESS_TOKEN = os.getenv("OPEN_AIRE_REFRESH_ACCESS_TOKEN")
        response_token = requests.get(
            "https://services.openaire.eu/uoa-user-management/api/users/getAccessToken?refreshToken="
            + OPEN_AIRE_REFRESH_ACCESS_TOKEN
        )

        if response_token.status_code == 200:
            OpenAire._openaire_token = response_token.json()["access_token"]
        else:
            raise AbstractImportError("Invalid OpenAire Access Token")

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
                "Authorization": "Bearer " + OpenAire._openaire_token,
                "User-Agent": "PaNetExtractor/1.0.0 ("
                + OpenAire._USER_AGENT_MAIL
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
            response = OpenAire.call_open_aire(doi)
            json_response = response.json()
            results = json_response.get("results", [])

            if results and "descriptions" in results[0] and results[0]["descriptions"]:
                abstract = results[0]["descriptions"][0]
            else:
                abstract = "No abstract available"
        except (AbstractImportError, RateLimitError) as e:
            if isinstance(e, AbstractImportError):
                abstract = "No abstract available"
            else:
                raise RateLimitError(e.retry, "Too many requests")

        return abstract
