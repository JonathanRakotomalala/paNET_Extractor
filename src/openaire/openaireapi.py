
import time
import os

time_start = None


class AbstractImportError(Exception):
    def __init__(self,message="OpenAire Error"):
        self.message = message 
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
    
class RateLimitError(Exception):
    def __init__(self,retry,message="OpenAire Error"):
        self.retry = retry
        self.message = message 
        super().__init__(self.message)
    def __str__(self):
        return f'{self.message+self.retry}'

class OpenAire:
    import requests
    OPEN_AIRE_REFRESH_ACCESS_TOKEN = os.environ.get("OPEN_AIRE_REFRESH_ACCESS_TOKEN")
    
    response_token = requests.get("https://services.openaire.eu/uoa-user-management/api/users/getAccessToken?refreshToken="+OPEN_AIRE_REFRESH_ACCESS_TOKEN)

    if response_token.status_code == 200:
        TOKEN = response_token.json()["access_token"]
    else:
        raise AbstractImportError("Invalid OpenAire Access Token")
    
    def get_abstract_from_doi(doi):
        """
            get the abstract with openaire's api 

            Args:
                doi: a string that represent the digital object identifier

            Returns: 
                A string, the abstract of the publication

            Raise:
                RateLimitError: If the requests limit of openaire api is reached
                AbstractImportError: If failed to get the abstract


        """
        url_link = "https://api.openaire.eu/graph/v1/researchProducts?pid="+doi

        response = OpenAire.requests.get(url_link,headers={"Authorization":"Bearer "+OpenAire.TOKEN,"User-Agent":"PaNetExtractor/1.0.0 (jonathan.rakotomalala@esrf.fr)"})
        time_start = time.time()

        if response.status_code == 200 and response.json()['header']['numFound']>0:
            return response
        elif response.status_code ==429: 
            
            if "Retry-After" not in response.headers:
                #waiting time  = difference of the time of the request and the time of the request rounded to the upper hour
                waiting_time = (time_start+3600) - time_start
            else:
                waiting_time = int(response.headers["Retry-After"])
            raise RateLimitError(waiting_time,"Too many requests")
        else :
             print(response.status_code)
             raise AbstractImportError("Unable to extract abstract from DOI")
        


