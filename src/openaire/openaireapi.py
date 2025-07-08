import requests
class AbstractImportError(Exception):
    def __init__(self,message="OpenAire Error"):
        self.message = message 
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

class OpenAire:
    def get_abstract_from_doi(doi):
        url = "https://api.openaire.eu/graph/v1/researchProducts?pid="+doi

        response = requests.get(url)
        if response.status_code == 200 and response.json()['header']['numFound']>0:
            return response.json()['results'][0]['descriptions'][0]
        elif response.status_code ==429: 
            raise AbstractImportError("Wait N times")
        else :
             raise AbstractImportError("Unable to extract abstract from DOI")