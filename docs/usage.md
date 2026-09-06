# Using the Client and the CLI

There is a comprehensive <a href="https://api.iucnredlist.org/api-docs/index.html" target="_blank" title="Red List API reference">Red List API reference</a> that can be consulted to understand the API itself, and `iucn-redlist-api` is a very thin client around this API, with a public method for every API endpoint.

## Client

The client methods are fully documented in the [API client reference](reference/api-client-reference), with example snippets. A more detailed client usage guide may be added at some point in the future.

An equivalent, but easier way of using `iucn-redlist-api` may be as a command line tool. This is described in more detail below.

## CLI

`iucn-redlist-api` can be used as a CLI (`redlist-cli`) to make command line requests to the Red List API, via the API client, with responses in JSON. This is described below - there is no separate CLI command reference as it is fairly simple and easy to use.

### Installation

The `redlist-cli` becomes available when the project is installed as a package, i.e. from PyPI, [non-editable mode](getting-started#non-editable-installation) or [editable mode](getting-started#editable-installation) mode, as described above.

!!! note
    You don't need an editable installation, unless you wish to evaluate and contribute changes via pull requests (PR)s.

All commands make [API](https://api.iucnredlist.org/api-docs/index.html) requests, and require the API key to be available in the environment, which can be done by setting an `API_KEY` environment variable, e.g. a simple command line export in Linux / MacOS:
```shell
export API_KEY="<Red List API key>"
```

If you don't have an API key, register a (non-commercial) account/profile on the [Red List API portal](https://api.iucnredlist.org/) and get the key from your profile.

### Command Tree & Help

On installing, the top-level `redlist-cli` command becomes available, and invoking it without any flags, produces a top-level (sub)command and (sub)command group listing:
```shell
Usage: redlist-cli [OPTIONS] COMMAND [ARGS]...

  IUCN Red List (of Threatened Species) API command line interface (CLI).

Options:
  --debug  Global CLI debug mode - can be overridden in individual request-
           level commands
  --help   Show this message and exit.

Commands:
  api-version             Red List API version
  assessment-search       Searches for assessment data based on search...
  assessments             Extinction risk assessments
  biogeographical-realms  Biogeographical realms
  comprehensive-groups    Comprehensive groups
  conservation-actions    Conservation actions
  countries               Countries (country names and ISO alpha-2 codes)
  faos                    Food and Agriculture Organization (FAO)...
  green-status            Species green status (status of recovery and...
  growth-forms            Growth forms
  habitats                Habitats
  information             Red List and Red List API information
  population-trends       Population trends
  red-list-categories     Red List extinction risk categories
  red-list-version        Red List version
  research                Research categories
  scopes                  Geographic assessment scopes
  statistics              Assessment statistics
  stresses                Species stress factors
  systems                 Ecosystems data
  taxa                    Taxa
  threats                 Species threat factors data
  use-and-trade           Species use and trade factors data
```

The command tree structure reflects the API structure, which is also reflected in the structure of the [API client methods](api-client-reference#iucn_redlist_api.api.IucnRedListApiClient).

Invoke any (sub)command group or (sub)command without any flags to see its help menu, e.g. taxa:
```shell
redlist-cli taxa
```
```shell
Usage: redlist-cli taxa [OPTIONS] COMMAND [ARGS]...

  Taxa.

Options:
  --help  Show this message and exit.

Commands:
  class                         Classes
  family                        Families
  kingdom                       Kingdoms
  order                         Orders
  phylum                        Phylums
  possibly-extinct              Possibly extinct taxa
  possibly-extinct-in-the-wild  Taxa that are possibly extinct in the wild
  scientific-name               Requests related to taxa using scientific...
  sis                           Taxa based on Species Information Service...
```

All non-group commands produce JSON responses, which could be empty depending on whether there was a request or response error. Ordinarily no error codes are displayed - in the case of an empty response check the endpoint in the API reference and your command invocation.

### Basic Examples

A selection of some specific examples, with individual commands and command outputs (abbreviated where they are too long) listed separately below each other, is shown below.

#### Red List and API Information

Getting high-level information, such as the API version:
```shell
redlist-cli api-version
```
```shell
{
    "api_version": "v4"
}
```
and the Red List version:
```shell
redlist-cli red-list-version
```
```shell
{
    "red_list_version": "2026-1"
}
```

#### (Extinction Risk of Species) Assessments

Getting all Red List assessments for a particular species, the <a href="https://www.iucnredlist.org/species/22696033/203852137" target="_new" title="IUCN Red List summary of the tawny eagle (Aquila rapax)">tawny eagle (*Aquila rapax*)</a>:
```shell
redlist-cli taxa scientific-name --genus-name Aquila --species-name rapax
```
```shell
{
    "taxon": {
        "sis_id": 22696033,
        "scientific_name": "Aquila rapax",
        "species_taxa": [],
        "subpopulation_taxa": [],
        "infrarank_taxa": [],
        "kingdom_name": "ANIMALIA",
        "phylum_name": "CHORDATA",
        "class_name": "AVES",
        "order_name": "ACCIPITRIFORMES",
        "family_name": "ACCIPITRIDAE",
        "genus_name": "Aquila",
        "species_name": "rapax",
        "subpopulation_name": null,
        "infra_name": null,
        "authority": "(Temminck, 1828)",
        "species": true,
        "subpopulation": false,
        "infrarank": false,
        "ssc_groups": [
            {
                "name": "IUCN SSC Bird Red List Authority (BirdLife International)",
                "url": "https://datazone.birdlife.org/",
                "description": "Red List Authority Coordinator: Ian Burfield (ian.burfield@birdlife.org)"
            }
        ],
        ...
        ...
    },
    "assessments": [
        {
            "assessment_date": "2021-10-25T01:00:00.000+01:00",
            "year_published": "2022",
            "latest": true,
            "possibly_extinct": false,
            "possibly_extinct_in_the_wild": false,
            "sis_taxon_id": 22696033,
            "criteria": "C2a(i,ii); D",
            "url": "https://www.iucnredlist.org/species/22696033/208745904",
            "taxon_scientific_name": "Aquila rapax",
            "red_list_category_code": "CR",
            "assessment_id": 208745904,
            "scopes": [
                {
                    "description": {
                        "en": "Mediterranean"
                    },
                    "code": "4"
                }
            ]
        },
 		...
 		...
        {
            "assessment_date": "1988-05-01T01:00:00.000+01:00",
            "year_published": "1988",
            "latest": false,
            "possibly_extinct": false,
            "possibly_extinct_in_the_wild": false,
            "sis_taxon_id": 22696033,
            "criteria": null,
            "url": "https://www.iucnredlist.org/species/22696033/23886797",
            "taxon_scientific_name": "Aquila rapax",
            "red_list_category_code": "LR/lc",
            "assessment_id": 23886797,
            "scopes": [
                {
                    "description": {
                        "en": "Global"
                    },
                    "code": "1"
                }
            ]
        }
    ],
    "params": {
        "genus_name": "Aquila",
        "species_name": "rapax"
    }
}
```

!!! note

    For assessment-related endpoints that produce a response JSON containing an `"assessments"` section, the assessments may not be in chronological order (either from the most recent to the oldest, or vice versa). And there is no API-level parameter that can be set directly in the request to ensure this. But this can always be achieved with some additional Python steps if using the [API client](api-client-reference#iucn_redlist_api.api.IucnRedListApiClient): capture the JSON in a dict, and sort the `assessments` section by the `"assessment_date"` key.

#### Red List (Extinction Risk) Categories

Getting all Red List categories used to assess extinction risks:
```shell
redlist-cli red-list-categories get
```
```shell
{
    "red_list_categories": [
        {
            "version": "Earlier Version",
            "description": {
                "en": "Abundant"
            },
            "code": "A"
        },
        {
            "version": "2.3",
            "description": {
                "en": "Critically Endangered"
            },
            "code": "CR"
        },
        ...
        ...
        {
            "version": "2.3",
            "description": {
                "en": "Vulnerable"
            },
            "code": "VU"
        }
    ]
}
```

#### Assessment Count

Getting a count of all species with Red List assessments:
```shell
redlist-cli statistics count
```
```
{
    "count": 175909
}
```
!!! note

    A stated IUCN Red List <a href="https://www.iucnredlist.org/about/barometer-of-life" target="_blank" title="IUCN Red List Barometer of Life">goal</a> is to increase the number of assessed species to **260000**.

#### Threat Factors

Getting all species threat factors:
```shell
redlist-cli threats get
```
```shell
{
    "threats": [
        {
            "description": {
                "en": "Residential & commercial development"
            },
            "code": "1"
        },
        {
            "description": {
                "en": "Housing & urban areas"
            },
            "code": "1_1"
        },
        ...
        ...
        {
            "description": {
                "en": "Other threat"
            },
            "code": "12_1"
        }
    ]
}
```

#### Stress Factors

Getting all species stress factors:
```shell
redlist-cli stresses get
```
```shell
{
    "stresses": [
        {
            "description": {
                "en": "Ecosystem stresses"
            },
            "code": "1"
        },
        {
            "description": {
                "en": "Ecosystem conversion"
            },
            "code": "1_1"
        },
        {
            "description": {
                "en": "Ecosystem degradation"
            },
            "code": "1_2"
        },
        ...
        ...
        },
        {
            "description": {
                "en": "Reduced reproductive success"
            },
            "code": "2_3_7"
        },
        {
            "description": {
                "en": "Other"
            },
            "code": "2_3_8"
        }
    ]
}
```

#### Possibly Extinct (and Possibly Extinct in the Wild) Status

Getting all Red List assessments that contain an indication of possibly extinct status:
```shell
redlist-cli taxa possibly-extinct
```
```shell
{
    "assessments": [
        {
            "assessment_date": "2011-08-22T01:00:00.000+01:00",
            "year_published": "2012",
            "latest": true,
            "possibly_extinct": true,
            "possibly_extinct_in_the_wild": false,
            "sis_taxon_id": 11058,
            "criteria": "B1ab(iii)",
            "url": "https://www.iucnredlist.org/species/11058/500479",
            "taxon_scientific_name": "Kubaryia pilikia",
            "red_list_category_code": "CR",
            "assessment_id": 500479,
            "scopes": [
                {
                    "description": {
                        "en": "Global"
                    },
                    "code": "1"
                }
            ]
        },
        ...
        ...
        {
            "assessment_date": "2009-11-19T00:00:00.000+00:00",
            "year_published": "2014",
            "latest": true,
            "possibly_extinct": true,
            "possibly_extinct_in_the_wild": false,
            "sis_taxon_id": 164808,
            "criteria": "B2ab(v)",
            "url": "https://www.iucnredlist.org/species/164808/1075123",
            "taxon_scientific_name": "Islamia pseudorientalica",
            "red_list_category_code": "CR",
            "assessment_id": 1075123,
            "scopes": [
                {
                    "description": {
                        "en": "Global"
                    },
                    "code": "1"
                },
                {
                    "description": {
                        "en": "Mediterranean"
                    },
                    "code": "4"
                }
            ]
        }
    ]
}
```

The command for possibly extinct in the wild status is almost identical:
```shell
redlist-cli taxa possibly-extinct-in-the-wild
```

#### Country Assessments

Getting all available assessments for Australia 🇦🇺 published in 20205 that contain species indications of possibly extinct status:
```shell
redlist-cli countries get-assessments --country-code AU --year-published 2025 --possibly-extinc
{
    "country": {
        "description": {
            "en": "Australia"
        },
        "code": "AU"
    },
    "assessments": [
        {
            "assessment_date": "2023-06-01T01:00:00.000+01:00",
            "year_published": "2025",
            "latest": true,
            "possibly_extinct": true,
            "possibly_extinct_in_the_wild": false,
            "sis_taxon_id": 221324039,
            "criteria": "B1ab(iii)+2ab(iii)",
            "url": "https://www.iucnredlist.org/species/221324039/235751186",
            "taxon_scientific_name": "Tympanocryptis mccartneyi",
            "red_list_category_code": "CR",
            "assessment_id": 235751186,
            "code": "AU",
            "code_type": "country",
            "scopes": [
                {
                    "description": {
                        "en": "Global"
                    },
                    "code": "1"
                }
            ]
        }
    ],
    "filters": {
        "year_published": "2025",
        "possibly_extinct": "True"
    }
}
```

#### Green (Recovery and Conservation) Status of Species

Getting all available green status assessments of species:
```shell
redlist-cli green-status get-all
```
```shell
{
    "assessments": [
        {
            "assessment_year": "2024",
            "weights": "Default",
            "justification": "The Chestnut-breasted Partridge (<em>Arborophila mandellii</em>) is assessed as having an Indeterminate recovery status because data on its current distribution and status are extremely limited. It's presence in China and Myanmar is inferred based on distribution modelling, with no documented sightings, making its presence in these countries uncertain. It is known to occur and is likely Viable in India and Bhutan. Due to the uncertainty in the species' current status and a lack of information on conservation impacts, all the Conservation Impact Metrics are assessed as Indeterminate. The species enjoys legal protection and area protection in some parts of its range, and it is possible that its status would be worse without these measures. In northeast India, there is work underway to establish community-conserved areas with ecotourism schemes as an alternative livelihood to hunting, which may improve the species' prospects in this region. More research and monitoring is required to determine the state of this species and necessary conservation actions. Until more is known, long-term prospects will remain uncertain.<br/><br/>For additional data, see the <a href=\"https://www.iucnredlist.org/resources/gss-supplementary\">Supplementary Information</a> document.",
            "species_recovery_category": "Indeterminate",
            "species_recovery_score_best": "50%",
    ...
    ...
                "synonyms": [
                    {
                        "name": "Diomedea demersa Linnaeus, 1758",
                        "status": "ACCEPTED",
                        "genus_name": "Diomedea",
                        "species_name": "demersa",
                        "species_author": "Linnaeus, 1758",
                        "infrarank_author": null,
                        "subpopulation_name": null,
                        "infra_type": null,
                        "infra_name": null
                    }
                ]
            }
        }
    ]
}
```

#### A Note on Data Capture and Export

The JSON response streams in the CLI console output can be captured quickly in Linux/MacOS/WSL by redirection to file, e.g.
```shell
redlist-cli green-status get-all > ./green-status.json
```

Depending on your requirements, the JSON data can then be exported to other formats such as CSV or Excel. If you're comfortable on the command line with JSON stream parsing tools such as [`jq`](https://jqlang.org/) you can also do this directly, with the additional use of Python and [Pandas](https://pandas.pydata.org), e.g. to CSV:
```shell
redlist-cli taxa possibly-extinct-in-the-wild | jq '.["assessments"]' > possibly-ew.json && \
python3 -c "import pandas as pd; pd.read_json('./possibly-ew.json').to_csv('./possibly-ew.csv', index=False)"
```
and Excel:
```shell
redlist-cli taxa possibly-extinct-in-the-wild | jq '.["assessments"]' > possibly-ew.json && \
python3 -c "import pandas as pd; pd.read_json('./possibly-ew.json').to_excel('./possibly-ew.xlsx', index=True)"
```

!!! note

    The Excel example requires [`openpyxl`](https://pypi.org/project/openpyxl/) to be installed in the working environment, and both examples require `jq` and Pandas.

You can also of course capture the response JSON streams manually by copying them directly into files, and using other applications to manually export the data into the desired formats.

#### Debug Mode

There is a global debug mode flag (defaulting to `False`) you can set for `redlist-cli`, which can also be overridden in the request-level commands, e.g.:
```shell
redlist-cli taxa phylum get --debug
```
```shell
2026-09-06 03:20:56 [DEBUG] iucn_redlist_api.api: Requesting URL: https://api.iucnredlist.org/api/v4/taxa/phylum
2026-09-06 03:20:56 [DEBUG] urllib3.connectionpool: Starting new HTTPS connection (1): api.iucnredlist.org:443
2026-09-06 03:20:56 [DEBUG] urllib3.connectionpool: https://api.iucnredlist.org:443 "GET /api/v4/taxa/phylum HTTP/1.1" 200 297
2026-09-06 03:20:56 [DEBUG] iucn_redlist_api.api: Response 200: {'Date': 'Sun, 06 Sep 2026 02:20:56 GMT', 'Content-Type'
...
{
    "phylum_names": [
        "ANNELIDA",
        "ANTHOCEROTOPHYTA",
        "ARTHROPODA",
        "ASCOMYCOTA",
        "BASIDIOMYCOTA",
        "BRYOPHYTA",
        "CHAROPHYTA",
        "CHLOROPHYTA",
        "CHORDATA",
        "CNIDARIA",
        "ECHINODERMATA",
        "HETEROKONTOPHYTA",
        "MARCHANTIOPHYTA",
        "MOLLUSCA",
        "NEMERTEA",
        "ONYCHOPHORA",
        "PLATYHELMINTHES",
        "PORIFERA",
        "RHODOPHYTA",
        "TRACHEOPHYTA"
    ]
}
```
