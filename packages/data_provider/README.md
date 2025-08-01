# data-provider
## The data-provider make requests to openaire's search products api to extract data from a doi

### Usage

A refresh access token and a mail passed onto environment variables for openaire requests:
OPEN_AIRE_REFRESH_ACCESS_TOKEN and USER_AGENT_MAIL


```console
    > from panet_technique_matcher import Openaire
    > Openaire()
```   


#### call_open_aire
```console
    > Openaire.call_open_aire("")
```

#### get_abstract_from_doi
```console
   > Openaire.get_abstract_from_doi("")
```
