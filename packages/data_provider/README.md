# data-provider
## The data-provider make requests to openaire's search products api to extract data from a doi

### Usage

> Requires refresh access token from openaire (expires after 1 month) and a mail passed onto environment variables for openaire requests:
OPEN_AIRE_REFRESH_ACCESS_TOKEN and USER_AGENT_MAIL


```console
    > from panet_technique_matcher import Openaire
    #Initialize openaire requests
    > Openaire()
```   


#### call_open_aire
```console
    > Openaire.call_open_aire("10.1038/s41563-023-01669-z")
```

#### get_abstract_from_doi
```console
   > abstract = Openaire.get_abstract_from_doi("10.1038/s41563-023-01669-z")
   > print(abstracts)
   "<jats:title>Abstract</jats:title><jats:p>Zeolitic imidazolate frameworks (ZIFs) are a subset of metal–organic frameworks with more than 200 characterized crystalline and amorphous networks made of divalent transition metal centres (for example, Zn<jats:sup>2+</jats:sup> and Co<jats:sup>2+</jats:sup>) linked by imidazolate linkers. ZIF thin films have been intensively pursued, motivated by the desire to prepare membranes for selective gas and liquid separations. To achieve membranes with high throughput, as in ångström-scale biological channels with nanometre-scale path lengths, ZIF films with the minimum possible thickness—down to just one unit cell—are highly desired. However, the state-of-the-art methods yield membranes where ZIF films have thickness exceeding 50 nm. Here we report a crystallization method from ultradilute precursor mixtures, which exploits registry with the underlying crystalline substrate, yielding (within minutes) crystalline ZIF films with thickness down to that of a single structural building unit (2 nm). The film crystallized on graphene has a rigid aperture made of a six-membered zinc imidazolate coordination ring, enabling high-permselective H<jats:sub>2</jats:sub> separation performance. The method reported here will probably accelerate the development of two-dimensional metal–organic framework films for efficient membrane separation.</jats:p>"
```
