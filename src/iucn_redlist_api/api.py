from __future__ import annotations

__all__ = [
    "IucnRedListApiClient",
    "IucnRedListApiResponse",
    "IucnRedListApiSession",
]


# -- IMPORTS --

# -- Standard libraries --
import json
import logging
import sys
import typing
from urllib.parse import urlencode

# -- 3rd party libraries --
import requests
from requests.models import Response

# -- Internal libraries --
from iucn_redlist_api.constants import IUCN_RED_LIST_API_CONSTANTS as API_CONSTANTS
from iucn_redlist_api.exceptions import IucnRedListApiRequestException


class IucnRedListApiClient:
    """Client for the IUCN Red List (of Threatened Species) API (v4).

    Consult the API documentation/reference for further details.

    https://api.iucnredlist.org/api-docs/index.html

    Obtain an API key from the API portal:

    https://api.iucnredlist.org/

    Examples
    --------
    Import the client class and create a new instance with an API key from the environment.

    >>> import json, os
    >>> client = IucnRedListApiClient(os.environ['API_KEY'])
    >>> client
    IucnRedListApiClient(api_version="v4", debug_mode=False)
    >>> assert client.api_session.api_key == os.environ['API_KEY']
    >>> client.get("information/api_version").json
    {'api_version': 'v4'}
    >>> client.get("information/red_list_version").json
    {'red_list_version': '2026-1'}

    Show biogeographical realms.

    >>> client.get_biogeographical_realms().json   # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    {'biogeographical_realms': [{'description': {'en': 'Afrotropical'},
       'code': '0'},
      {'description': {'en': 'Antarctic'}, 'code': '1'},
      {'description': {'en': 'Australasian'}, 'code': '2'},
      {'description': {'en': 'Indomalayan'}, 'code': '3'},
      {'description': {'en': 'Nearctic'}, 'code': '4'},
      {'description': {'en': 'Neotropical'}, 'code': '5'},
      {'description': {'en': 'Oceanian'}, 'code': '6'},
      {'description': {'en': 'Palearctic'}, 'code': '7'}]}

    Show kingdom taxa.

    >>> client.get_taxa_kingdom().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    {'kingdom_names': ['ANIMALIA', 'CHROMISTA', 'FUNGI', 'PLANTAE']}

    Get the latest data and assessments for the Tawny Eagle (Aquila rapax).

    >>> client.get_taxa_scientific_name_assessments('Aquila', 'rapax').json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    {'taxon': {'sis_id': 22696033,
      'scientific_name': 'Aquila rapax',
      'species_taxa': [],
      'subpopulation_taxa': [],
      'infrarank_taxa': [],
      'kingdom_name': 'ANIMALIA',
      'phylum_name': 'CHORDATA',
      'class_name': 'AVES',
      'order_name': 'ACCIPITRIFORMES',
      'family_name': 'ACCIPITRIDAE',
      'genus_name': 'Aquila',
      'species_name': 'rapax',
      'subpopulation_name': None,
      'infra_name': None,
      'authority': '(Temminck, 1828)',
      'species': True,
      'subpopulation': False,
      'infrarank': False,
      ...
      ...
      {'assessment_date': '1988-05-01T01:00:00.000+01:00',
       'year_published': '1988',
       'latest': False,
       'possibly_extinct': False,
       'possibly_extinct_in_the_wild': False,
       'sis_taxon_id': 22696033,
       'criteria': None,
       'url': 'https://www.iucnredlist.org/species/22696033/23886797',
       'taxon_scientific_name': 'Aquila rapax',
       'red_list_category_code': 'LR/lc',
       'assessment_id': 23886797,
       'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
     'params': {'genus_name': 'Aquila', 'species_name': 'rapax'}}

    Turn on debug mode logging with ``debug=True`` when creating the client:

    >>> client = IucnRedListApiClient(os.environ['API_KEY'], debug_mode=True)
    >>> client.get_taxa_kingdom().json  # doctest: +SKIP
    2026-09-02 20:46:49 [DEBUG] api: Requesting URL: https://api.iucnredlist.org/api/v4/taxa/kingdom
    2026-09-02 20:46:49 [DEBUG] urllib3.connectionpool: https://api.iucnredlist.org:443 "GET /api/v4/taxa/kingdom HTTP/1.1" 200 60
    2026-09-02 20:46:49 [DEBUG] iucn_redlist_api.api: Response 200: {'Date': 'Wed, 02 Sep 2026 19:46:49 GMT', 'Content-Type': 'application/json', 'Content-Length': '60', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0, private, must-revalidate', 'content-security-policy': "default-src 'self'; script-src 'self' https://static.cloudflareinsights.com https://cloud.umami.is https://ksbk62v4jgjkcqo3vmgzxqvu.agents.do-ai.run https://d1bxh8uas1mnw7.cloudfront.net https://embed.altmetric.com https://api.altmetric.com 'unsafe-inline' 'unsafe-eval'; style-src 'self' https://unpkg.com 'unsafe-inline'; img-src 'self' data: https://iucnredlist.org https://*.iucnredlist.org https://*.digitaloceanspaces.com https://*.tile.openstreetmap.org https://static.inaturalist.org https://www.inaturalist.org https://*.amazonaws.com https://server.arcgisonline.com https://badges.altmetric.com; font-src 'self'; object-src 'none'; connect-src 'self' https://api-gateway.umami.dev https://gateway.umami.is https://ksbk62v4jgjkcqo3vmgzxqvu.agents.do-ai.run; frame-src https://www.youtube.com https://www.youtube-nocookie.com https://ksbk62v4jgjkcqo3vmgzxqvu.agents.do-ai.run https://cloud.umami.is https://iucnredlist.appsignal-status.com; frame-ancestors 'none'; form-action 'self'", 'etag': 'W/"986f7acb982a486adecfac980e922872"', 'feature-policy': "camera 'none'; gyroscope 'none'; microphone 'none'; usb 'none'; fullscreen 'none'; payment 'none'", 'strict-transport-security': 'max-age=31556952; includeSubDomains', 'vary': 'Accept-Encoding', 'x-cache': 'miss', 'x-request-id': '96234488-1675-4a30-8cf8-74fcab3a7229', 'x-runtime': '0.015784', 'Nel': '{"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}', 'cf-cache-status': 'DYNAMIC', 'Speculation-Rules': '"/cdn-cgi/speculation"', 'Report-To': '{"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=wUp0QCFY9j4WLVt5qAFQaeRTMtMGyPLPt9XY9hwLc9ksawM7dWDIcf0eIBr21OHAS4QmSuAto6bXp4%2FyEW%2Bv4NFnjMPYZktRX0Do96uKjmlfpPUaGqs1jTk%2BQcwzq16333wSISc%3D"}]}', 'Server': 'cloudflare', 'CF-RAY': 'a34f05e41915e034-CPH'}
    Out[86]: {'kingdom_names': ['ANIMALIA', 'CHROMISTA', 'FUNGI', 'PLANTAE']}

    Note that toggling debug mode on/off in an existing client is not supported. Create a new client if you want to change debug mode.
    """

    # All instances have thse private attributes
    _api_session: IucnRedListApiSession
    _debug_mode: bool = False

    def _set_logging(self, debug_mode: bool) -> bool:
        """Processes client-requested debug mode appropriately.

        No file handlers are set.
        """
        if not debug_mode:
            logging.basicConfig(handlers=[], force=True)
            return False

        logging.getLogger("asyncio").setLevel(logging.WARNING)
        self._logger = logging.getLogger(__name__)
        if not self._logger.handlers:
            logging.basicConfig(
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                level=logging.DEBUG,
                stream=sys.stdout,
            )
            return True

    def __init__(self, api_key: str, /, *, debug_mode: bool | None = False) -> None:
        """Initialiser requiring the API key.

        Parameters
        ----------
        api_key : str
            The API key obtained from the registration profile on the developer
            portal.

        debug_mode : bool, default=False
            Optional debug mode that controls whether all requests and responses
            are logged to the console, at the level of URLs and header
            information - response data are not logged.

        Examples
        --------
        >>> import os; from iucn_redlist_api.constants import IUCN_RED_LIST_API_CONSTANTS as API_CONSTANTS
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client
        IucnRedListApiClient(api_version="v4", debug_mode=False)
        >>> assert client.api_session.api_key == os.environ['API_KEY']
        >>> assert client.api_session.headers == {'Accept': 'application/json', 'Authorization': os.environ['API_KEY']}
        >>> client.api_version
        'v4'
        """
        self._api_session = IucnRedListApiSession(api_key)

        # Note that debug mode is handled initially, once per client lifecycle.
        # Toggling debug mode on/off in a client is not supported. If you want
        # to toggle it create a new client with the desired debug mode.
        self._debug_mode = self._set_logging(debug_mode)

    @property
    def api_session(self) -> IucnRedListApiSession:
        """The API session instance.

        Returns
        -------
        IucnRedListApiSession
            The current API session object.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> assert client.api_session
        """
        return self._api_session

    @property
    def api_version(self) -> str:
        """The API version used by the client.

        Returns
        -------
        str
            The API version used by the client.

        Examples
        --------
        >>> import os; from iucn_redlist_api.constants import IUCN_RED_LIST_API_CONSTANTS as API_CONSTANTS
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.api_version
        'v4'
        """
        return API_CONSTANTS.API_VERSION.value

    def __repr__(self) -> str:
        return f'IucnRedListApiClient(api_version="{self.api_version}", debug_mode={self._debug_mode})'

    def _filter_params(self, **params: typing.Any) -> dict[str, typing.Any]:
        """A params dict with null or empty parameters removed.

        Parameters
        ----------
        **params
            Optional key-value param pairs.

        Returns
        -------
        dict
            The processed params dict with null-valued or empty params removed.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client._filter_params(A="a", B=None, C="c")
        {'A': 'a', 'C': 'c'}
        >>> client._filter_params(A="a", B="b", C="c")
        {'A': 'a', 'B': 'b', 'C': 'c'}
        >>> client._filter_params(A="a", B="b", C=[])
        {'A': 'a', 'B': 'b'}
        """
        if not params:
            return {}

        return {key: val for key, val in params.items() if val}

    def get(
        self, endpoint: str, /, *, params: dict[str, typing.Any] | None = None
    ) -> IucnRedListApiResponse:
        """The raw response from the request.

        This is the base client handler for all Red List API requests. It does
        not normally need to be used directly, as there is a public client
        method for each Red List API endpoint.

        Leading or trailing forward slashes (``"/"``) are stripped, but no
        attempt is made to enforce case sensitivity: lower cased endpoints
        and parameter names are assumed.

        Parameters
        ----------
        endpoint : str
            The full endpoint, excluding parameters - which should be specified
            separately - and without the base URL (as that is determined in this
            method) or leading or trailing forward-slashes (``"/"``).

        params : dict, default=None
            Optional dict of parameter keys and values, defaults to ``None``
            in which case no parameters are passed in the request URL.

        Returns
        -------
        IucnRedListApiResponse
            The API response.

        Raises
        ------
        IucnRedListApiRequestException
            If there was a [requests.RequestException][] in making the original
            request.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get("information/api_version").json
        {'api_version': 'v4'}
        >>> client.get("information/red_list_version").json
        {'red_list_version': '2026-1'}
        >>> client.get("assessment_search", params={"filter_on[]": ["eu_27_post_2020_endemic", "amazing"]}).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessment_ids': [220151895, 218695618, 229002159, 137843212], 'filters': {'filter_on': ['eu_27_post_2020_endemic', 'amazing']}}
        """
        _endpoint = endpoint.strip("/")

        if params:
            iterable_parameter_values = bool(
                [
                    v
                    for v in params.values()
                    if not isinstance(v, str) and isinstance(v, typing.Iterable)
                ]
            )
            params_str = urlencode(params, doseq=iterable_parameter_values)
            url = f"{API_CONSTANTS.BASEURL.value}/{_endpoint}?{params_str}"
        else:
            url = f"{API_CONSTANTS.BASEURL.value}/{_endpoint}"

        if self._debug_mode:
            self._logger.debug(f"Requesting URL: {url}")

        try:
            res = IucnRedListApiResponse(self.api_session.get(url))
        except requests.RequestException as e:
            raise IucnRedListApiRequestException(e)

        if self._debug_mode:
            self._logger.debug(f"Response {res.status_code}: {res.headers}")

        return res

    # ------------------------------------------------------------------------#
    # --- Assessments --------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_assessment(self, assessment_id: int) -> IucnRedListApiResponse:
        """Assessment data for a specific assessment ID.

        Implements the request:

            GET /api/v4/assessment/{assessment_id}

        The assessment ID can be current or historic. A list of all current and
        historic assessment IDs can be be obtained by

        Parameters
        ----------
        assessment_id : int
            Assessment ID.

        Returns
        -------
        IucnRedListApiResponse
            The assessment data for the given assessment ID.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_assessment(259841783).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessment_date': '2024-05-17T01:00:00.000+01:00',
         'year_published': '2026',
         'latest': True,
         'possibly_extinct': False,
         'possibly_extinct_in_the_wild': False,
         'sis_taxon_id': 97238174,
         'criteria': 'B1b(ii,iii)+2b(ii,iii)',
         'url': 'https://www.iucnredlist.org/species/97238174/259841783',
         'citation': 'van Deijk, J., Parsons, M., van Swaay, C. & Sterling, P. 2026. Noctua carvalhoi. The IUCN Red List of Threatened Species 2026: e.T97238174A259841783. Accessed on 02 September 2026.',
         'assessment_id': 259841783,
         'assessment_points': False,
         'assessment_ranges': True,
         'taxon': {'sis_id': 97238174,
          'scientific_name': 'Noctua carvalhoi',
         ...
         ...
         'systems': [{'description': {'en': 'Terrestrial'}, 'code': '0'}]}
        """
        endpoint = f"assessment/{assessment_id}"

        return self.get(endpoint)

    def assessment_search(
        self, filter_on: str | list[str], page: int | None = None
    ) -> IucnRedListApiResponse:
        """Assessment data based on a search with optional search criteria.

        Implements the request:

            GET /api/v4/assessment_search

        Returns a paginated list of latest assessment IDs filtered according to the
        criteria specified with ``filter_on``.

        Parameters
        ----------
        filter_on : str or list
            A string or list of strings representing search criteria.

        page : int, default=None
            Optional page number, defaults to ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data filtered according to the given search
            criteria.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.assessment_search(filter_on=['eu_27_post_2020_endemic']).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessment_ids': [259841783,
          245042349,
          209243069,
          222394391,
          260113703,
          ...
          ...
          259836458],
         'filters': {'filter_on': ['eu_27_post_2020_endemic']}}
        """
        endpoint = "assessment_search"
        params = {
            "filter_on[]": filter_on,
        }
        if page:
            params.update({"page": page})

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Biogeographical realms ---------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_biogeographical_realms(self) -> IucnRedListApiResponse:
        """Biogeographical realms data.

        Implements the request:

            GET /api/v4/biogeographical_realms

        Returns
        -------
        IucnRedListApiResponse
            Response containing biogeographical realm data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_biogeographical_realms().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'biogeographical_realms': [{'description': {'en': 'Afrotropical'},
           'code': '0'},
          {'description': {'en': 'Antarctic'}, 'code': '1'},
          {'description': {'en': 'Australasian'}, 'code': '2'},
          {'description': {'en': 'Indomalayan'}, 'code': '3'},
          {'description': {'en': 'Nearctic'}, 'code': '4'},
          {'description': {'en': 'Neotropical'}, 'code': '5'},
          {'description': {'en': 'Oceanian'}, 'code': '6'},
          {'description': {'en': 'Palearctic'}, 'code': '7'}]}
        """
        endpoint = "biogeographical_realms"

        return self.get(endpoint)

    def get_biogeographical_realm_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a biogeographical realm by realm code.

        Implements the request:

            GET /api/v4/biogeographical_realms/{code}

        Biogeographical realm codes can be obtained with
        [`IucnRedListApiClient.get_biogeographical_realms`][iucn_redlist_api.api.IucnRedListApiClient.get_biogeographical_realms].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A biogeographical realm code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given biogeographical realm.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_biogeographical_realm_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'biogeographical_realm': {'description': {'en': 'Antarctic'}, 'code': '1'},
         'assessments': [{'assessment_date': '2009-03-28T00:00:00.000+00:00',
           'year_published': '2012',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 162502,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/162502/903824',
           'taxon_scientific_name': 'Stoloteuthis leucoptera',
           'red_list_category_code': 'DD',
           'assessment_id': 903824,
           'code': '1',
           'code_type': 'biogeographical_realm',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
        ...
        ...
        {'assessment_date': '2008-06-30T01:00:00.000+01:00',
           'year_published': '2008',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 2477,
           'criteria': 'A1abd',
           'url': 'https://www.iucnredlist.org/species/2477/9447146',
           'taxon_scientific_name': 'Balaenoptera musculus',
           'red_list_category_code': 'EN',
           'assessment_id': 9447146,
           'code': '1',
           'code_type': 'biogeographical_realm',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"biogeographical_realms/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Comprehensive groups -----------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_comprehensive_groups(self) -> IucnRedListApiResponse:
        """Comprehensive groups data.

        Implements the request:

            GET /api/v4/comprehensive_groups

        Returns
        -------
        IucnRedListApiResponse
            Response containing data about comprehensive groups.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_comprehensive_groups().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'comprehensive_group': [{'high': True,
           'comp': True,
           'name': 'amphibians',
           'higher_name': 'amphibians'},
          {'high': False,
           'comp': True,
           'name': 'angelfishes',
           'higher_name': 'selected_bony_fishes'},
                  ...
          ...
          {'high': True, 'comp': False, 'name': 'velvet_worms', 'higher_name': None}]}
        """
        endpoint = "comprehensive_groups"

        return self.get(endpoint)

    def get_comprehensive_group_assessments(
        self,
        name: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a comprehensive group by group name.

        Implements the request:

            GET /api/v4/comprehensive_groups/{code}

        Comprehensive groups data can be obtained with
        [`IucnRedListApiClient.get_comprehensive_groups`][iucn_redlist_api.api.IucnRedListApiClient.get_comprehensive_groups].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        name : str
            A comprehensive group name.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given comprehensive group.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_comprehensive_group_assessments('amphibians', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'comprehensive_group': {'high': True,
          'comp': True,
          'name': 'amphibians',
          'higher_name': 'amphibians'},
         'assessments': [{'assessment_date': None,
           'year_published': None,
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 2645,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/2645/291011390',
           'taxon_scientific_name': 'Telmatobius macrostomus',
           'red_list_category_code': 'N/A',
           'assessment_id': 291011390,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2025-01-20T00:00:00.000+00:00',
           'year_published': '2025',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 258941335,
           'criteria': 'B1ab(iii)+2ab(iii)',
           'url': 'https://www.iucnredlist.org/species/258941335/258941471',
           'taxon_scientific_name': 'Platypelis ando',
           'red_list_category_code': 'CR',
           'assessment_id': 258941471,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"comprehensive_groups/{name}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Conservation actions -----------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_conservation_actions(self) -> IucnRedListApiResponse:
        """Conservation actions data.

        Implements the request:

            GET /api/v4/conservation_actions

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for conservation actions.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_conservation_actions().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'conservation_actions': [{'description': {'en': 'Land/water protection'},
           'code': '1'},
          {'description': {'en': 'Site/area protection'}, 'code': '1_1'},
          {'description': {'en': 'Resource & habitat protection'}, 'code': '1_2'},
          {'description': {'en': 'Land/water management'}, 'code': '2'},
          ...
          ...
          {'description': {'en': 'Non-monetary values'}, 'code': '6_5'}]}
        """
        endpoint = "conservation_actions"

        return self.get(endpoint)

    def get_conservation_action_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a conservation action by action code.

        Implements the request:

            GET /api/v4/conservation_actions/{code}

        Conservation actions data can be obtained with
        [`IucnRedListApiClient.get_conservation_actions`][iucn_redlist_api.api.IucnRedListApiClient.get_conservation_actions].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A conservation action code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given conservation action.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_conservation_action_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'conservation_action': {'description': {'en': 'Land/water protection'},
          'code': '1'},
         'assessments': [],
         'filters': {}}
        """
        endpoint = f"conservation_actions/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Countries ----------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_countries(self) -> IucnRedListApiResponse:
        """Countries data including ISO alpha-2 country codes.

        Implements the request:

            GET /api/v4/countries

        Returns
        -------
        IucnRedListApiResponse
            Countries data including ISO alpha-2 country codes.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_countries().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'countries': [{'description': {'en': 'Andorra'}, 'code': 'AD'},
          {'description': {'en': 'United Arab Emirates'}, 'code': 'AE'},
          {'description': {'en': 'Afghanistan'}, 'code': 'AF'},
          {'description': {'en': 'Antigua and Barbuda'}, 'code': 'AG'},
          {'description': {'en': 'Anguilla'}, 'code': 'AI'},
          ...
          ...
          {'description': {'en': 'Zambia'}, 'code': 'ZM'},
          {'description': {'en': 'Zimbabwe'}, 'code': 'ZW'}]}
        """
        endpoint = "countries"

        return self.get(endpoint)

    def get_country_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a country by ISO alpha-2 country code.

        Implements the request:

            GET /api/v4/countries/{code}

        Countries data can be obtained with
        [`IucnRedListApiClient.get_countries`][iucn_redlist_api.api.IucnRedListApiClient.get_countries].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            An ISO alpha-2 country code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given country.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_country_assessments('AD', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'country': {'description': {'en': 'Andorra'}, 'code': 'AD'},
         'assessments': [{'assessment_date': '2016-02-18T00:00:00.000+00:00',
           'year_published': '2016',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 12835,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/12835/510082',
           'taxon_scientific_name': 'Marmota marmota',
           'red_list_category_code': 'LC',
           'assessment_id': 510082,
           'code': 'AD',
           'code_type': 'country',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'},
            {'description': {'en': 'Europe'}, 'code': '2'}]},
          ...
          ...
          {'assessment_date': '2013-04-15T01:00:00.000+01:00',
           'year_published': '2013',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 203219,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/203219/2762397',
           'taxon_scientific_name': 'Gentiana cruciata',
           'red_list_category_code': 'LC',
           'assessment_id': 2762397,
           'code': 'AD',
           'code_type': 'country',
           'scopes': [{'description': {'en': 'Europe'}, 'code': '2'}]}],
        'filters': {}}

        """
        endpoint = f"countries/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- FAOs ---------------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_faos(self) -> IucnRedListApiResponse:
        """Food and Agriculture Organization (FAO) international fishing areas data, including FAO codes.

        Implements the request:

            GET /api/v4/faos

        Returns
        -------
        IucnRedListApiResponse
            Food and Agriculture Organization (FAO) international fishing areas
            data, including FAO codes.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_faos().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'faos': [{'description': {'en': 'Arctic Sea'}, 'code': '18'},
          {'description': {'en': 'Atlantic - northwest'}, 'code': '21'},
          {'description': {'en': 'Atlantic - northeast'}, 'code': '27'},
          {'description': {'en': 'Atlantic - western central'}, 'code': '31'},
          {'description': {'en': 'Atlantic - eastern central'}, 'code': '34'},
          {'description': {'en': 'Mediterranean and Black Sea'}, 'code': '37'},
          {'description': {'en': 'Atlantic - southwest'}, 'code': '41'},
          {'description': {'en': 'Atlantic - southeast'}, 'code': '47'},
          {'description': {'en': 'Atlantic - Antarctic'}, 'code': '48'},
          {'description': {'en': 'Indian Ocean - western'}, 'code': '51'},
          {'description': {'en': 'Indian Ocean - eastern'}, 'code': '57'},
          {'description': {'en': 'Indian Ocean - Antarctic'}, 'code': '58'},
          {'description': {'en': 'Pacific - northwest'}, 'code': '61'},
          {'description': {'en': 'Pacific - northeast'}, 'code': '67'},
          {'description': {'en': 'Pacific - western central'}, 'code': '71'},
          {'description': {'en': 'Pacific - eastern central'}, 'code': '77'},
          {'description': {'en': 'Pacific - southwest'}, 'code': '81'},
          {'description': {'en': 'Pacific - southeast'}, 'code': '87'},
          {'description': {'en': 'Pacific - Antarctic'}, 'code': '88'}]}
        """
        endpoint = "faos"

        return self.get(endpoint)

    def get_fao_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for an FAO international fishing area by FAO code.

        Implements the request:

            GET /api/v4/faos/{code}

        FAO data can be obtained with
        [`IucnRedListApiClient.get_faos`][iucn_redlist_api.api.IucnRedListApiClient.get_faos].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            An FAO international fishing area code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given FAO international fishing area.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_fao_assessments('18', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'fao': {'description': {'en': 'Arctic Sea'}, 'code': '18'},
         'assessments': [{'assessment_date': '2019-08-29T01:00:00.000+01:00',
           'year_published': '2021',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 161403,
           'criteria': 'A2bd',
           'url': 'https://www.iucnredlist.org/species/161403/887942',
           'taxon_scientific_name': 'Somniosus pacificus',
           'red_list_category_code': 'NT',
           'assessment_id': 887942,
           'code': '18',
           'code_type': 'fao',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2016-02-05T00:00:00.000+00:00',
           'year_published': '2016',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 15106,
           'criteria': 'A3c',
           'url': 'https://www.iucnredlist.org/species/15106/45228501',
           'taxon_scientific_name': 'Odobenus rosmarus',
           'red_list_category_code': 'VU',
           'assessment_id': 45228501,
           'code': '18',
           'code_type': 'fao',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"faos/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Growth forms -------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_growth_forms(self) -> IucnRedListApiResponse:
        """Growth forms data.

        Implements the request:

            GET /api/v4/growth_forms

        Returns
        -------
        IucnRedListApiResponse
            Growth forms data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_growth_forms().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'growth_forms': [{'description': {'en': 'Annual'}, 'code': 'A'},
          {'description': {'en': 'Moss'}, 'code': 'B'},
          {'description': {'en': 'Cycad'}, 'code': 'C'},
          {'description': {'en': 'Epiphyte'}, 'code': 'E'},
          {'description': {'en': 'Forb or Herb'}, 'code': 'F'},
          {'description': {'en': 'Geophyte'}, 'code': 'GE'},
          {'description': {'en': 'Graminoid'}, 'code': 'GR'},
          {'description': {'en': 'Hydrophyte'}, 'code': 'H'},
          {'description': {'en': 'Lithophyte'}, 'code': 'L'},
          {'description': {'en': 'Lichen'}, 'code': 'LC'},
          {'description': {'en': 'Fungus'}, 'code': 'M'},
          {'description': {'en': 'Parasite'}, 'code': 'P'},
          {'description': {'en': 'Fern'}, 'code': 'PT'},
          {'description': {'en': 'Shrub - size unknown'}, 'code': 'S'},
          {'description': {'en': 'Succulent - annual'}, 'code': 'SA'},
          {'description': {'en': 'Succulent - form unknown'}, 'code': 'SC'},
          {'description': {'en': 'Succulent - shrub'}, 'code': 'SH'},
          {'description': {'en': 'Shrub - large'}, 'code': 'SL'},
          {'description': {'en': 'Shrub - small'}, 'code': 'SS'},
          {'description': {'en': 'Succulent - tree'}, 'code': 'ST'},
          {'description': {'en': 'Tree - size unknown'}, 'code': 'T'},
          {'description': {'en': 'Tree - large'}, 'code': 'TL'},
          {'description': {'en': 'Tree - small'}, 'code': 'TS'},
          {'description': {'en': 'Vines'}, 'code': 'V'}]}
        """
        endpoint = "growth_forms"

        return self.get(endpoint)

    def get_growth_form_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a growth form by growth form code.

        Implements the request:

            GET /api/v4/growth_forms/{code}

        Growth forms data can be obtained with
        [`IucnRedListApiClient.get_growth_forms`][iucn_redlist_api.api.IucnRedListApiClient.get_growth_forms].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A growth form code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given growth form.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_growth_form_assessments('A', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'growth_form': {'description': {'en': 'Annual'}, 'code': 'A'},
         'assessments': [{'assessment_date': '2008-04-23T01:00:00.000+01:00',
           'year_published': '2020',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 157955,
           'criteria': 'B2ab(iii)',
           'url': 'https://www.iucnredlist.org/species/157955/754465',
           'taxon_scientific_name': 'Oxygonum subfastigiatum',
           'red_list_category_code': 'CR',
           'assessment_id': 754465,
           'code': 'A',
           'code_type': 'growth_form',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2013-03-23T00:00:00.000+00:00',
           'year_published': '2013',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 179577,
           'criteria': 'B2ab(i,ii,iii,v)c(iv)',
           'url': 'https://www.iucnredlist.org/species/179577/1583123',
           'taxon_scientific_name': 'Marsilea botryocarpa',
           'red_list_category_code': 'EN',
           'assessment_id': 1583123,
           'code': 'A',
           'code_type': 'growth_form',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"growth_forms/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Green status -------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_green_status_all(self) -> IucnRedListApiResponse:
        """The green status of species.

        Implements the request:

            GET /api/v4/green_status/all

        Returns
        -------
        IucnRedListApiResponse
            Green status of species data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_green_status_all().json  # doctest: +SKIP
        {'assessments': [{'assessment_year': '2024',
           'weights': 'Default',
           'justification': 'The Chestnut-breasted Partridge (<em>Arborophila mandellii</em>) is assessed as having an Indeterminate recovery status because data on its current distribution and status are extremely limited. It\'s presence in China and Myanmar is inferred based on distribution modelling, with no documented sightings, making its presence in these countries uncertain. It is known to occur and is likely Viable in India and Bhutan. Due to the uncertainty in the species\' current status and a lack of information on conservation impacts, all the Conservation Impact Metrics are assessed as Indeterminate. The species enjoys legal protection and area protection in some parts of its range, and it is possible that its status would be worse without these measures. In northeast India, there is work underway to establish community-conserved areas with ecotourism schemes as an alternative livelihood to hunting, which may improve the species\' prospects in this region. More research and monitoring is required to determine the state of this species and necessary conservation actions. Until more is known, long-term prospects will remain uncertain.<br/><br/>For additional data, see the <a href="https://www.iucnredlist.org/resources/gss-supplementary">Supplementary Information</a> document.',
           'species_recovery_category': 'Indeterminate',
        ...
        ...
        'synonyms': [{'name': 'Diomedea demersa Linnaeus, 1758',
          'status': 'ACCEPTED',
          'genus_name': 'Diomedea',
          'species_name': 'demersa',
          'species_author': 'Linnaeus, 1758',
          'infrarank_author': None,
          'subpopulation_name': None,
          'infra_type': None,
          'infra_name': None}]}}]}
        """
        endpoint = "green_status/all"

        return self.get(endpoint)

    # ------------------------------------------------------------------------#
    # --- Habitats -----------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_habitats(self) -> IucnRedListApiResponse:
        """Habitats data.

        Implements the request:

            GET /api/v4/habitats

        Returns
        -------
        IucnRedListApiResponse
            Habitats data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_habitats().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'habitats': [{'description': {'en': 'Forest'}, 'code': '1'},
          {'description': {'en': 'Forest - Boreal'}, 'code': '1_1'},
          {'description': {'en': 'Forest - Subarctic'}, 'code': '1_2'},
          {'description': {'en': 'Forest - Subantarctic'}, 'code': '1_3'},
          {'description': {'en': 'Forest - Temperate'}, 'code': '1_4'},
          {'description': {'en': 'Forest - Subtropical/Tropical Dry'}, 'code': '1_5'},
          ...
          ...
          {'description': {'en': 'Artificial/Marine - Mariculture Cages'}, 'code': '15_12'},
          {'description': {'en': 'Artificial/Marine - Mari/Brackishculture Ponds'}, 'code': '15_13'},
          {'description': {'en': 'Introduced vegetation'}, 'code': '16'},
          {'description': {'en': 'Other'}, 'code': '17'},
          {'description': {'en': 'Unknown'}, 'code': '18'}]}
        """
        endpoint = "habitats"

        return self.get(endpoint)

    def get_habitat_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a habitat by habitat code.

        Implements the request:

            GET /api/v4/habitats/{code}

        Habitats data can be obtained with
        [`IucnRedListApiClient.get_habitats`][iucn_redlist_api.api.IucnRedListApiClient.get_habitats].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A habitat code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given habitat.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_habitat_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'habitat': {'description': {'en': 'Forest'}, 'code': '1'},
         'assessments': [{'assessment_date': '2008-01-01T00:00:00.000+00:00',
           'year_published': '2008',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 133958,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/133958/3881104',
           'taxon_scientific_name': 'Thaipotamon lomkao',
           'red_list_category_code': 'LC',
           'assessment_id': 3881104,
           'code': '1',
           'code_type': 'habitat',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2016-01-28T00:00:00.000+00:00',
           'year_published': '2017',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 19945,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/19945/121711379',
           'taxon_scientific_name': 'Scapteromys tumidus',
           'red_list_category_code': 'LC',
           'assessment_id': 121711379,
           'code': '1',
           'code_type': 'habitat',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
        'filters': {}}
        """
        endpoint = f"habitats/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Information --------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_information_api_version(self) -> IucnRedListApiResponse:
        """The current Red List API version.

        Implements the request:

            GET /api/v4/information/api_version

        Returns
        -------
        IucnRedListApiResponse
            Current Red List API version.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_information_api_version().json
        {'api_version': 'v4'}
        """
        endpoint = "information/api_version"

        return self.get(endpoint)

    def get_information_red_list_version(self) -> IucnRedListApiResponse:
        """The current Red List version.

        Implements the request:

            GET /api/v4/information/red_list_version

        Returns
        -------
        IucnRedListApiResponse
            Current Red List version.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_information_red_list_version().json
        {'red_list_version': '2026-1'}
        """
        endpoint = "information/red_list_version"

        return self.get(endpoint)

    # ------------------------------------------------------------------------#
    # --- Population trends --------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_population_trends(self) -> IucnRedListApiResponse:
        """Ppulation trends data.

        Implements the request:

            GET /api/v4/population_trends

        Returns
        -------
        IucnRedListApiResponse
            Population trends data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_population_trends().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'population_trends': [{'description': {'en': 'Increasing'}, 'code': '0'},
          {'description': {'en': 'Decreasing'}, 'code': '1'},
          {'description': {'en': 'Stable'}, 'code': '2'},
          {'description': {'en': 'Unknown'}, 'code': '3'}]}
        """
        endpoint = "population_trends"

        return self.get(endpoint)

    def get_population_trend_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a population trend by trend code.

        Implements the request:

            GET /api/v4/population_trends/{code}

        Population trends data can be obtained with
        [`IucnRedListApiClient.get_population_trends`][iucn_redlist_api.api.IucnRedListApiClient.get_population_trends].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A population trend code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given population trend.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_population_trend_assessments('0', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'population_trend': {'description': {'en': 'Increasing'}, 'code': '0'},
         'assessments': [{'assessment_date': '2023-03-01T00:00:00.000+00:00',
           'year_published': '2025',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 13053,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/13053/512056',
           'taxon_scientific_name': 'Melanosuchus niger',
           'red_list_category_code': 'LC',
           'assessment_id': 512056,
           'code': '0',
           'code_type': 'population_trend',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2009-11-18T00:00:00.000+00:00',
           'year_published': '2013',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 40836,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/40836/2935666',
           'taxon_scientific_name': 'Mammillaria guelzowiana',
           'red_list_category_code': 'LC',
           'assessment_id': 2935666,
           'code': '0',
           'code_type': 'population_trend',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"population_trends/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Red List categories ------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_red_list_categories(self) -> IucnRedListApiResponse:
        """Red List categories data.

        Implements the request:

            GET /api/v4/red_list_categories

        Returns
        -------
        IucnRedListApiResponse
            Response containing Red List categories data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_red_list_categories().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'red_list_categories': [{'version': 'Earlier Version',
           'description': {'en': 'Abundant'},
           'code': 'A'},
          {'version': '2.3',
           'description': {'en': 'Critically Endangered'},
           'code': 'CR'},
          {'version': '3.1',
           'description': {'en': 'Critically Endangered'},
           'code': 'CR'},
          ...
          ...
          {'version': '3.1', 'description': {'en': 'Vulnerable'}, 'code': 'VU'},
          {'version': '2.3', 'description': {'en': 'Vulnerable'}, 'code': 'VU'}]}
        """
        endpoint = "red_list_categories"

        return self.get(endpoint)

    def get_red_list_category_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a Red List category by category code.

        Implements the request:

            GET /api/v4/red_list_categories/{code}

        Red List categories data can be obtained with
        [`IucnRedListApiClient.get_red_list_categories`][iucn_redlist_api.api.IucnRedListApiClient.get_red_list_categories].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A Red List category code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given Red List category.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_red_list_category_assessments('A', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'red_list_category': [{'version': 'Earlier Version',
           'description': {'en': 'Abundant'},
           'code': 'A'}],
         'assessments': [{'assessment_date': '1990-01-01T00:00:00.000+00:00',
           'year_published': '1990',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 13323,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/13323/3642907',
           'taxon_scientific_name': 'Microcebus murinus',
           'red_list_category_code': 'A',
           'assessment_id': 3642907,
           'code': 'A',
           'code_type': 'red_list_category',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"red_list_categories/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Research -----------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_research(self) -> IucnRedListApiResponse:
        """Research categories data.

        Implements the request:

            GET /api/v4/research

        Returns
        -------
        IucnRedListApiResponse
            Research categories data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_research().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'research': [{'description': {'en': 'Research'}, 'code': '1'},
          {'description': {'en': 'Taxonomy'}, 'code': '1_1'},
          {'description': {'en': 'Population size, distribution & trends'},
           'code': '1_2'},
          {'description': {'en': 'Life history & ecology'}, 'code': '1_3'},
          {'description': {'en': 'Harvest, use & livelihoods'}, 'code': '1_4'},
          {'description': {'en': 'Threats'}, 'code': '1_5'},
          {'description': {'en': 'Actions'}, 'code': '1_6'},
          {'description': {'en': 'Conservation Planning'}, 'code': '2'},
          {'description': {'en': 'Species Action/Recovery Plan'}, 'code': '2_1'},
          {'description': {'en': 'Area-based Management Plan'}, 'code': '2_2'},
          {'description': {'en': 'Harvest & Trade Management Plan'}, 'code': '2_3'},
          {'description': {'en': 'Monitoring'}, 'code': '3'},
          {'description': {'en': 'Population trends'}, 'code': '3_1'},
          {'description': {'en': 'Harvest level trends'}, 'code': '3_2'},
          {'description': {'en': 'Trade trends'}, 'code': '3_3'},
          {'description': {'en': 'Habitat trends'}, 'code': '3_4'},
          {'description': {'en': 'Other'}, 'code': '4'}]}
        """
        endpoint = "research"

        return self.get(endpoint)

    def get_research_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a research category by research code.

        Implements the request:

            GET /api/v4/research/{code}

        Research categories data can be obtained with
        [`IucnRedListApiClient.get_research`][iucn_redlist_api.api.IucnRedListApiClient.get_research].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A research category code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given research category.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_research_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'research': {'description': {'en': 'Research'}, 'code': '1'},
         'assessments': [{'assessment_date': '2017-02-01T00:00:00.000+00:00',
           'year_published': '2019',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 122380888,
           'criteria': 'B1ab(i,ii,iii,v)+2ab(i,ii,iii,v)',
           'url': 'https://www.iucnredlist.org/species/122380888/122414905',
           'taxon_scientific_name': 'Xerochlamys itremoensis',
           'red_list_category_code': 'EN',
           'assessment_id': 122414905,
           'code': '1',
           'code_type': 'research',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
           ...
           ...
         'filters': {}}
        """
        endpoint = f"research/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Scopes -------------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_scopes(self) -> IucnRedListApiResponse:
        """Geographical assessment scopes data.

        Implements the request:

            GET /api/v4/scopes

        Returns
        -------
        IucnRedListApiResponse
            Geographical assessment scopes data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_scopes().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'scopes': [{'description': {'en': 'Global'}, 'code': '1'},
          {'description': {'en': 'Europe'}, 'code': '2'},
          {'description': {'en': 'Mediterranean'}, 'code': '4'},
          {'description': {'en': 'Western Africa'}, 'code': '8'},
          {'description': {'en': 'S. Africa FW'}, 'code': '9'},
          {'description': {'en': 'Pan-Africa'}, 'code': '10'},
          {'description': {'en': 'Central Africa'}, 'code': '16'},
          {'description': {'en': 'Northeastern Africa'}, 'code': '17'},
          {'description': {'en': 'Eastern Africa'}, 'code': '18'},
          {'description': {'en': 'Northern Africa'}, 'code': '21'},
          {'description': {'en': 'Gulf of Mexico'}, 'code': '45433062'},
          {'description': {'en': 'Caribbean'}, 'code': '45433063'},
          {'description': {'en': 'Persian Gulf'}, 'code': '45433064'},
          {'description': {'en': 'Arabian Sea'}, 'code': '100765562'}]}
        """
        endpoint = "scopes"

        return self.get(endpoint)

    def get_scope_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a geographical assessment scope by scope code.

        Implements the request:

            GET /api/v4/scopes/{code}

        Scopes data can be obtained with
        [`IucnRedListApiClient.get_scopes`][iucn_redlist_api.api.IucnRedListApiClient.get_scopes].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A geographical assessment scope code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given geographical assessment scope.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_scope_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'scope': {'description': {'en': 'Global'}, 'code': '1'},
         'assessments': [{'assessment_date': '2019-11-21T00:00:00.000+00:00',
           'year_published': '2020',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 10030,
           'criteria': 'A2bd',
           'url': 'https://www.iucnredlist.org/species/10030/495630',
           'taxon_scientific_name': 'Hexanchus griseus',
           'red_list_category_code': 'NT',
           'assessment_id': 495630,
           'code': '1',
           'code_type': 'scope',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2016-05-25T01:00:00.000+01:00',
           'year_published': '2016',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 136503,
           'criteria': 'B2ab(iii)',
           'url': 'https://www.iucnredlist.org/species/136503/518549',
           'taxon_scientific_name': 'Plecotus sardus',
           'red_list_category_code': 'VU',
           'assessment_id': 518549,
           'code': '1',
           'code_type': 'scope',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'},
            {'description': {'en': 'Europe'}, 'code': '2'},
            {'description': {'en': 'Mediterranean'}, 'code': '4'}]}],
         'filters': {}}
        """
        endpoint = f"scopes/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Statistics ---------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_statistics_count(self) -> IucnRedListApiResponse:
        """A count of the number of species with assessments.

        Implements the request:

            GET /api/v4/statistics/count

        Returns
        -------
        IucnRedListApiResponse
            Response containing a count of the number of species with assessments.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_statistics_count().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'count': 175909}
        """
        endpoint = "statistics/count"

        return self.get(endpoint)

    # ------------------------------------------------------------------------#
    # --- Stresses -----------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_stresses(self) -> IucnRedListApiResponse:
        """Species stress factors data.

        Implements the request:

            GET /api/v4/stresses

        Returns
        -------
        IucnRedListApiResponse
            Species stress factors data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_stresses().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'stresses': [{'description': {'en': 'Ecosystem stresses'}, 'code': '1'},
          {'description': {'en': 'Ecosystem conversion'}, 'code': '1_1'},
          {'description': {'en': 'Ecosystem degradation'}, 'code': '1_2'},
          {'description': {'en': 'Indirect ecosystem effects'}, 'code': '1_3'},
          {'description': {'en': 'Species Stresses'}, 'code': '2'},
          {'description': {'en': 'Species mortality'}, 'code': '2_1'},
          {'description': {'en': 'Species disturbance'}, 'code': '2_2'},
          {'description': {'en': 'Indirect species effects'}, 'code': '2_3'},
          {'description': {'en': 'Hybridisation'}, 'code': '2_3_1'},
          {'description': {'en': 'Competition'}, 'code': '2_3_2'},
          {'description': {'en': 'Loss of mutualism'}, 'code': '2_3_3'},
          {'description': {'en': 'Loss of pollinator'}, 'code': '2_3_4'},
          {'description': {'en': 'Inbreeding'}, 'code': '2_3_5'},
          {'description': {'en': 'Skewed sex ratios'}, 'code': '2_3_6'},
          {'description': {'en': 'Reduced reproductive success'}, 'code': '2_3_7'},
          {'description': {'en': 'Other'}, 'code': '2_3_8'}]}
        """
        endpoint = "stresses"

        return self.get(endpoint)

    def get_stress_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a species stress factor by stress code.

        Implements the request:

            GET /api/v4/stresses/{code}

        Species stress factors can be obtained with
        [`IucnRedListApiClient.get_stresses`][iucn_redlist_api.api.IucnRedListApiClient.get_stresses].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A species stress factor code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given species stress factor.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_stress_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'stress': {'description': {'en': 'Ecosystem stresses'}, 'code': '1'},
         'assessments': [{'assessment_date': '2021-03-29T01:00:00.000+01:00',
           'year_published': '2023',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 165302,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/165302/1080229',
           'taxon_scientific_name': 'Potamotrygon constellata',
           'red_list_category_code': 'DD',
           'assessment_id': 1080229,
           'code': '1',
           'code_type': 'stress',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2024-06-14T01:00:00.000+01:00',
           'year_published': '2024',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 22712616,
           'criteria': 'A2c+3c+4c',
           'url': 'https://www.iucnredlist.org/species/22712616/260306457',
           'taxon_scientific_name': 'Microtarsus melanoleucos',
           'red_list_category_code': 'NT',
           'assessment_id': 260306457,
           'code': '1',
           'code_type': 'stress',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"stresses/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Systems ------------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_systems(self) -> IucnRedListApiResponse:
        """Ecosystems data.

        Implements the request:

            GET /api/v4/systems

        Returns
        -------
        IucnRedListApiResponse
            Ecosystems data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_systems().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'systems': [{'description': {'en': 'Terrestrial'}, 'code': '0'},
          {'description': {'en': 'Freshwater (=Inland waters)'}, 'code': '1'},
          {'description': {'en': 'Marine'}, 'code': '2'}]}
        """
        endpoint = "systems"

        return self.get(endpoint)

    def get_system_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for an ecosystem by ecosystem code.

        Implements the request:

            GET /api/v4/systems/{code}

        Ecosystems data can be obtained with
        [`IucnRedListApiClient.get_systems`][iucn_redlist_api.api.IucnRedListApiClient.get_systems].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            An ecosystem code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given ecosystem.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_system_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'system': {'description': {'en': 'Freshwater (=Inland waters)'}, 'code': '1'},
         'assessments': [{'assessment_date': '2018-03-13T00:00:00.000+00:00',
           'year_published': '2021',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 10041,
           'criteria': 'A2cd+4cd',
           'url': 'https://www.iucnredlist.org/species/10041/495907',
           'taxon_scientific_name': 'Heosemys annandalii',
           'red_list_category_code': 'CR',
           'assessment_id': 495907,
           'code': '1',
           'code_type': 'system',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2012-03-05T00:00:00.000+00:00',
           'year_published': '2012',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 155517,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/155517/731938',
           'taxon_scientific_name': 'Viviparus viviparus',
           'red_list_category_code': 'LC',
           'assessment_id': 731938,
           'code': '1',
           'code_type': 'system',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"systems/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Taxa ---------------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_taxa_sis_assessments(self, sis_id: int, /) -> IucnRedListApiResponse:
        """Assessment data for a specific taxon in the Species Identification Service (SIS) system by SIS ID.

        Implements the request:

            GET /api/v4/taxa/sis/{sis_id}

        The SIS ID can be current or historic.

        Parameters
        ----------
        sis_id : int
            Species Information Service (SIS) ID of the associated taxon.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given taxon.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_sis_assessments(158189).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'sis_id': 158189,
         'taxon': {'sis_id': 158189,
          'scientific_name': 'Sphaeranthus cristatus',
          ...
          ...
         'assessments': [{'assessment_date': '2006-11-02T00:00:00.000+00:00',
           'year_published': '2020',
           'latest': True,
           'possibly_extinct': True,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 158189,
           'criteria': 'B2ab(iii); D',
           'url': 'https://www.iucnredlist.org/species/158189/765782',
           'taxon_scientific_name': 'Sphaeranthus cristatus',
           'red_list_category_code': 'CR',
           'assessment_id': 765782,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}]}
        """
        endpoint = f"taxa/sis/{sis_id}"

        return self.get(endpoint)

    def get_taxa_scientific_name_assessments(
        self,
        genus_name: str,
        species_name: str,
        /,
        *,
        infra_name: str | None = None,
        subpopulation_name: str | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a species (or sub-species) by scientific name (in binomial, or trinomial nomenclature).

        Implements the request:

            GET /api/v4/taxa/scientific_name

        The scientific name can be specified either as a combination of genus
        name and species name (binomial nomenclature), or the genus name,
        species name and an infraspecific taxon name (trinomial nomenclature).

        Scientific name variables are treated case insensitively.

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        genus_name : str
            Genus name.

        species_name : str
            Species name.

        infra_name : str, default=None
            Optional infraspecific taxon name, defaults to ``None``.

        subpopulation_name : str, default=None
            Optional subpopulation name, defaults to ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given species (or sub-species).

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_scientific_name_assessments('Aquila', 'rapax').json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'taxon': {'sis_id': 22696033,
          'scientific_name': 'Aquila rapax',
          'species_taxa': [],
          'subpopulation_taxa': [],
          'infrarank_taxa': [],
          'kingdom_name': 'ANIMALIA',
          'phylum_name': 'CHORDATA',
          'class_name': 'AVES',
          'order_name': 'ACCIPITRIFORMES',
          'family_name': 'ACCIPITRIDAE',
          'genus_name': 'Aquila',
          'species_name': 'rapax',
          'subpopulation_name': None,
          'infra_name': None,
          'authority': '(Temminck, 1828)',
          'species': True,
          'subpopulation': False,
          'infrarank': False,
          ...
          ...
          {'assessment_date': '1988-05-01T01:00:00.000+01:00',
           'year_published': '1988',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 22696033,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/22696033/23886797',
           'taxon_scientific_name': 'Aquila rapax',
           'red_list_category_code': 'LR/lc',
           'assessment_id': 23886797,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'params': {'genus_name': 'Aquila', 'species_name': 'rapax'}}
        """
        endpoint = "taxa/scientific_name"
        params = self._filter_params(
            genus_name=genus_name,
            species_name=species_name,
        )

        return self.get(endpoint, params=params)

    def get_taxa_kingdom(self) -> IucnRedListApiResponse:
        """Kingdom taxa data.

        Implements the request:

            GET /api/v4/taxa/kingdom

        Returns
        -------
        IucnRedListApiResponse
            Kingdom taxa data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_kingdom().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'kingdom_names': ['ANIMALIA', 'CHROMISTA', 'FUNGI', 'PLANTAE']}
        """
        endpoint = "taxa/kingdom"

        return self.get(endpoint)

    def get_taxa_kingdom_assessments(
        self,
        kingdom_name: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a given kingdom by kingdom name.

        Implements the request:

            GET /api/v4/taxa/kingdom/{kingdom_name}

        Kingdom names can be obtained with
        [`IucnRedListApiClient.get_taxa_kingdom`][iucn_redlist_api.api.IucnRedListApiClient.get_taxa_kingdom].

        Kingdom names are treated case insensitively.

        Any optional parameters that are null are dropped from the request

        Parameters
        ----------
        kingdom_name : str
            Kingdom name.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given kingdom.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_kingdom_assessments('Animalia', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessments': [{'assessment_date': '2019-11-21T00:00:00.000+00:00',
           'year_published': '2020',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 10030,
           'criteria': 'A2bd',
           'url': 'https://www.iucnredlist.org/species/10030/495630',
           'taxon_scientific_name': 'Hexanchus griseus',
           'red_list_category_code': 'NT',
           'assessment_id': 495630,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2016-05-21T01:00:00.000+01:00',
           'year_published': '2016',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 136536,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/136536/518646',
           'taxon_scientific_name': 'Microtus brachycercus',
           'red_list_category_code': 'LC',
           'assessment_id': 518646,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'},
            {'description': {'en': 'Europe'}, 'code': '2'},
            {'description': {'en': 'Mediterranean'}, 'code': '4'}]}],
         'filters': {'kingdom_name': 'Animalia'}}
        """
        endpoint = f"taxa/kingdom/{kingdom_name}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    def get_taxa_phylum(self) -> IucnRedListApiResponse:
        """Phylum taxa data.

        Implements the request:

            GET /api/v4/taxa/phylum

        Returns
        -------
        IucnRedListApiResponse
            Phylum taxa data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_phylum().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'phylum_names': ['ANNELIDA',
          'ANTHOCEROTOPHYTA',
          'ARTHROPODA',
          'ASCOMYCOTA',
          'BASIDIOMYCOTA',
          'BRYOPHYTA',
          'CHAROPHYTA',
          'CHLOROPHYTA',
          'CHORDATA',
          'CNIDARIA',
          'ECHINODERMATA',
          'HETEROKONTOPHYTA',
          'MARCHANTIOPHYTA',
          'MOLLUSCA',
          'NEMERTEA',
          'ONYCHOPHORA',
          'PLATYHELMINTHES',
          'PORIFERA',
          'RHODOPHYTA',
          'TRACHEOPHYTA']}
        """
        endpoint = "taxa/phylum"

        return self.get(endpoint)

    def get_taxa_phylum_assessments(
        self,
        phylum_name: str,
        /,
        *,
        year_published: int | None = None,
        latest: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a given phylum by phylum name.

        Implements the request:

            GET /api/v4/taxa/phylum/{phylum_name}

        Phylum names can be obtained with
        [`IucnRedListApiClient.get_taxa_phylum`][iucn_redlist_api.api.IucnRedListApiClient.get_taxa_phylum].

        Phylum names are treated case insensitively.

        Any optional parameters that are null are dropped from the request

        Parameters
        ----------
        phylum_name : str
            Phylum name.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given phylum.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_phylum_assessments('Annelida', latest=True).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessments': [{'assessment_date': '1996-08-01T01:00:00.000+01:00',
           'year_published': '1996',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 12418,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/12418/3341675',
           'taxon_scientific_name': 'Lutodrilus multivesiculatus',
           'red_list_category_code': 'LR/nt',
           'assessment_id': 3341675,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2016-12-10T00:00:00.000+00:00',
           'year_published': '2017',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 103132762,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/103132762/103193255',
           'taxon_scientific_name': 'Graliophilus parvus',
           'red_list_category_code': 'LC',
           'assessment_id': 103193255,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {'latest': 'True', 'phylum_name': 'Annelida'}}
        """
        endpoint = f"taxa/phylum/{phylum_name}"
        params = self._filter_params(
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    def get_taxa_class(self) -> IucnRedListApiResponse:
        """Class taxa data.

        Implements the request:

            GET /api/v4/taxa/class

        Returns
        -------
        IucnRedListApiResponse
            Class taxa data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_class().json['class_names'][:10]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        ['ACTINOPTERYGII',
         'AGARICOMYCETES',
         'AMPHIBIA',
         'ANDREAEOPSIDA',
         'ANTHOCEROTOPSIDA',
         'ANTHOZOA',
         'ARACHNIDA',
         'ARTHONIOMYCETES',
         'ASTEROIDEA',
         'AVES']
        """
        endpoint = "taxa/class"

        return self.get(endpoint)

    def get_taxa_class_assessments(
        self,
        class_name: str,
        /,
        *,
        year_published: int | None = None,
        latest: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a given class by phylum name.

        Implements the request:

            GET /api/v4/taxa/class/{class_name}

        Class names can be obtained with
        [`IucnRedListApiClient.get_taxa_class`][iucn_redlist_api.api.IucnRedListApiClient.get_taxa_class].

        Class names are treated case insensitively.

        Any optional parameters that are null are dropped from the request

        Parameters
        ----------
        class_name : str
            Class name.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given class.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_class_assessments('Aves', latest=True).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessments': [{'assessment_date': '2015-03-31T01:00:00.000+01:00',
           'year_published': '2015',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 22693621,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/22693621/69555490',
           'taxon_scientific_name': 'Haematopus meadewaldoi',
           'red_list_category_code': 'EX',
           'assessment_id': 69555490,
           'scopes': [{'description': {'en': 'Europe'}, 'code': '2'}]},
          ...
          ...
          {'assessment_date': '2017-10-01T01:00:00.000+01:00',
           'year_published': '2017',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 22701577,
           'criteria': 'B2ab(i,ii,iii,iv,v); C2a(i)',
           'url': 'https://www.iucnredlist.org/species/22701577/118816985',
           'taxon_scientific_name': 'Herpsilochmus pectoralis',
           'red_list_category_code': 'VU',
           'assessment_id': 118816985,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {'latest': 'True', 'class_name': 'Aves'}}
        """
        endpoint = f"taxa/class/{class_name}"
        params = self._filter_params(
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    def get_taxa_order(self) -> IucnRedListApiResponse:
        """Order taxa data.

        Implements the request:

            GET /api/v4/taxa/order

        Returns
        -------
        IucnRedListApiResponse
            Order taxa data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_order().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'order_names': ['ACAROSPORALES',
          'ACCIPITRIFORMES',
          'ACIPENSERIFORMES',
          'ACOCHLIDIIMORPHA',
          'ACORALES',
          ...
          ...
          'ZEIFORMES',
          'ZINGIBERALES',
          'ZOANTHARIA',
          'ZORAPTERA',
          'ZYGOPHYLLALES']}
        """
        endpoint = "taxa/order"

        return self.get(endpoint)

    def get_taxa_order_assessments(
        self,
        order_name: str,
        /,
        *,
        year_published: int | None = None,
        latest: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a given order by order name.

        Implements the request:

            GET /api/v4/taxa/order/{order_name}

        Order names can be obtained with
        [`IucnRedListApiClient.get_taxa_order`][iucn_redlist_api.api.IucnRedListApiClient.get_taxa_order].

        Order names are treated case insensitively.

        Any optional parameters that are null are dropped from the request

        Parameters
        ----------
        order_name : str
            Order name.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given order.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_order_assessments('Acarosporales', latest=True).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessments': [{'assessment_date': '2020-06-10T01:00:00.000+01:00',
           'year_published': '2020',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 176075275,
           'criteria': 'D2',
           'url': 'https://www.iucnredlist.org/species/176075275/177005677',
           'taxon_scientific_name': 'Acarospora malouina',
           'red_list_category_code': 'VU',
           'assessment_id': 177005677,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {'latest': 'True', 'order_name': 'Acarosporales'}}
        """
        endpoint = f"taxa/order/{order_name}"
        params = self._filter_params(
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    def get_taxa_family(self) -> IucnRedListApiResponse:
        """Family taxa data.

        Implements the request:

            GET /api/v4/taxa/family

        Returns
        -------
        IucnRedListApiResponse
            Family taxa data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_family().json['family_names'][:10]  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        ['ABROCOMIDAE',
         'ACANTHACEAE',
         'ACANTHAMETROPODIDAE',
         'ACANTHISITTIDAE',
         'ACANTHIZIDAE',
         'ACANTHOCOCCIDAE',
         'ACANTHODRILIDAE',
         'ACANTHOGORGIIDAE',
         'ACANTHURIDAE',
         'ACAROSPORACEAE']
        """
        endpoint = "taxa/family"

        return self.get(endpoint)

    def get_taxa_family_assessments(
        self,
        family_name: str,
        /,
        *,
        year_published: int | None = None,
        latest: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a given family by family name.

        Implements the request:

            GET /api/v4/taxa/family/{family_name}

        Family names can be obtained with
        [`IucnRedListApiClient.get_taxa_family`][iucn_redlist_api.api.IucnRedListApiClient.get_taxa_family].

        Family names are treated case insensitively.

        Any optional parameters that are null are dropped from the request

        Parameters
        ----------
        family_name : str
            Family name.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            The assessment data for the given family.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_family_assessments('Abrocomidae', latest=True).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessments': [{'assessment_date': '2016-03-01T00:00:00.000+00:00',
           'year_published': '2016',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 136658,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/136658/22182152',
           'taxon_scientific_name': 'Cuscomys oblativa',
           'red_list_category_code': 'DD',
           'assessment_id': 22182152,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2016-03-01T00:00:00.000+00:00',
           'year_published': '2016',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 136302,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/136302/22182871',
           'taxon_scientific_name': 'Abrocoma uspallata',
           'red_list_category_code': 'DD',
           'assessment_id': 22182871,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {'latest': 'True', 'family_name': 'Abrocomidae'}}
        """
        endpoint = f"taxa/family/{family_name}"
        params = self._filter_params(
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    def get_taxa_possibly_extinct(self) -> IucnRedListApiResponse:
        """Data about possibly extinct taxa.

        Implements the request:

            GET /api/v4/taxa/possibly_extinct

        Returns
        -------
        IucnRedListApiResponse
            Data about taxa that are possibly extinct.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_possibly_extinct().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessments': [{'assessment_date': '2011-08-22T01:00:00.000+01:00',
           'year_published': '2012',
           'latest': True,
           'possibly_extinct': True,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 11058,
           'criteria': 'B1ab(iii)',
           'url': 'https://www.iucnredlist.org/species/11058/500479',
           'taxon_scientific_name': 'Kubaryia pilikia',
           'red_list_category_code': 'CR',
           'assessment_id': 500479,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2009-11-19T00:00:00.000+00:00',
           'year_published': '2014',
           'latest': True,
           'possibly_extinct': True,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 164808,
           'criteria': 'B2ab(v)',
           'url': 'https://www.iucnredlist.org/species/164808/1075123',
           'taxon_scientific_name': 'Islamia pseudorientalica',
           'red_list_category_code': 'CR',
           'assessment_id': 1075123,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'},
            {'description': {'en': 'Mediterranean'}, 'code': '4'}]}]}
        """
        endpoint = "taxa/possibly_extinct"

        return self.get(endpoint)

    def get_taxa_possibly_extinct_in_the_wild(self) -> IucnRedListApiResponse:
        """Data about taxa that are possibly extinct in the wild.

        Implements the request:

            GET /api/v4/taxa/possibly_extinct_in_the_wild

        Returns
        -------
        IucnRedListApiResponse
            Data about taxa that are possibly extinct in the wild.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_taxa_possibly_extinct_in_the_wild().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'assessments': [{'assessment_date': '2006-11-03T00:00:00.000+00:00',
           'year_published': '2020',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': True,
           'sis_taxon_id': 157997,
           'criteria': 'B2ab(iii); D',
           'url': 'https://www.iucnredlist.org/species/157997/756253',
           'taxon_scientific_name': 'Celosia patentiloba',
           'red_list_category_code': 'CR',
           'assessment_id': 756253,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2015-08-21T01:00:00.000+01:00',
           'year_published': '2015',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': True,
           'sis_taxon_id': 80174575,
           'criteria': 'D',
           'url': 'https://www.iucnredlist.org/species/80174575/80174614',
           'taxon_scientific_name': 'Phyllostegia parviflora var. lydgatei',
           'red_list_category_code': 'CR',
           'assessment_id': 80174614,
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}]}
        """
        endpoint = "taxa/possibly_extinct_in_the_wild"

        return self.get(endpoint)

    # ------------------------------------------------------------------------#
    # --- Threats ------------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_threats(self) -> IucnRedListApiResponse:
        """Species threat factors data.

        Implements the request:

            GET /api/v4/threats

        Returns
        -------
        IucnRedListApiResponse
            Species threat factors data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_threats().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'threats': [{'description': {'en': 'Residential & commercial development'},
           'code': '1'},
          {'description': {'en': 'Housing & urban areas'}, 'code': '1_1'},
          {'description': {'en': 'Commercial & industrial areas'}, 'code': '1_2'},
          {'description': {'en': 'Tourism & recreation areas'}, 'code': '1_3'},
          {'description': {'en': 'Agriculture & aquaculture'}, 'code': '2'},
          ...
          ...
          {'description': {'en': 'Temperature extremes'}, 'code': '11_3'},
          {'description': {'en': 'Storms & flooding'}, 'code': '11_4'},
          {'description': {'en': 'Other impacts'}, 'code': '11_5'},
          {'description': {'en': 'Other options'}, 'code': '12'},
          {'description': {'en': 'Other threat'}, 'code': '12_1'}]}
        """
        endpoint = "threats"

        return self.get(endpoint)

    def get_threat_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a species threat factor by threat code.

        Implements the request:

            GET /api/v4/threats/{code}

        Species threat data can be obtained with
        [`IucnRedListApiClient.get_threats`][iucn_redlist_api.api.IucnRedListApiClient.get_threats].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A species threat code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given species threat.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_threat_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'threat': {'description': {'en': 'Residential & commercial development'},
          'code': '1'},
         'assessments': [{'assessment_date': '2015-10-29T00:00:00.000+00:00',
           'year_published': '2016',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 107250449,
           'criteria': 'D2',
           'url': 'https://www.iucnredlist.org/species/107250449/107302977',
           'taxon_scientific_name': 'Eryngium fluminense',
           'red_list_category_code': 'VU',
           'assessment_id': 107302977,
           'code': '1',
           'code_type': 'threat',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
         ...
         ...
         'filters': {}}
        """
        endpoint = f"threats/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)

    # ------------------------------------------------------------------------#
    # --- Use and trade ------------------------------------------------------#
    # ------------------------------------------------------------------------#
    def get_use_and_trade(self) -> IucnRedListApiResponse:
        """Species use and trade factors data.

        Implements the request:

            GET /api/v4/use_and_trade

        Returns
        -------
        IucnRedListApiResponse
            Species use and trade factors data.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_use_and_trade().json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'use_and_trade': [{'description': {'en': 'Food - human'}, 'code': '1'},
          {'description': {'en': 'Food - animal'}, 'code': '2'},
          {'description': {'en': 'Medicine - human & veterinary'}, 'code': '3'},
          {'description': {'en': 'Poisons'}, 'code': '4'},
          {'description': {'en': 'Manufacturing chemicals'}, 'code': '5'},
          {'description': {'en': 'Other chemicals'}, 'code': '6'},
          {'description': {'en': 'Fuels'}, 'code': '7'},
          {'description': {'en': 'Fibre'}, 'code': '8'},
          {'description': {'en': 'Construction or structural materials'}, 'code': '9'},
          {'description': {'en': 'Wearing apparel, accessories'}, 'code': '10'},
          {'description': {'en': 'Other household goods'}, 'code': '11'},
          {'description': {'en': 'Handicrafts, jewellery, etc.'}, 'code': '12'},
          {'description': {'en': 'Pets/display animals, horticulture'}, 'code': '13'},
          {'description': {'en': 'Research'}, 'code': '14'},
          {'description': {'en': 'Sport hunting/specimen collecting'}, 'code': '15'},
          {'description': {'en': 'Establishing ex-situ production *'}, 'code': '16'},
          {'description': {'en': 'Other (free text)'}, 'code': '17'},
          {'description': {'en': 'Unknown'}, 'code': '18'}]}
        """
        endpoint = "use_and_trade"

        return self.get(endpoint)

    def get_use_and_trade_assessments(
        self,
        code: str,
        /,
        *,
        page: int | None = None,
        year_published: int | None = None,
        latest: bool | None = None,
        possibly_extinct: bool | None = None,
        possibly_extinct_in_the_wild: bool | None = None,
        scope_code: int | None = None,
    ) -> IucnRedListApiResponse:
        """Assessment data for a species use and trade factor by code.

        Implements the request:

            GET /api/v4/use_and_trade/{code}

        Species use and trade data can be obtained with
        [`IucnRedListApiClient.get_use_and_trade`][iucn_redlist_api.api.IucnRedListApiClient.get_use_and_trade].

        Any optional parameters that are null are dropped from the request.

        Parameters
        ----------
        code : str
            A species use and trade code.

        page : int, default=None
            Optional page number, defaults to ``None``.

        year_published : int, default=None
            Optional assessment publication year, defaults to ``None``.

        latest : bool, default=None
            Optional indicator of whether the latest assessment should be
            returned, defaults to ``None``.

        possibly_extinct : bool, default=None
            Optional indicator of species extinction, defaults to ``None``.

        possibly_extinct_in_the_wild : bool, default=None
            Optional indicator of species extinction in the wild, defaults to
            ``None``.

        scope_code : int, default=None
            Optional indicator of geographic assessment scope code, defaults to
            ``None``.

        Returns
        -------
        IucnRedListApiResponse
            Assessment data for the given species use and trade.

        Examples
        --------
        >>> import os
        >>> client = IucnRedListApiClient(os.environ['API_KEY'])
        >>> client.get_use_and_trade_assessments('1', page=1).json  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        {'use_and_trade': {'description': {'en': 'Food - human'}, 'code': '1'},
         'assessments': [{'assessment_date': '2019-11-21T00:00:00.000+00:00',
           'year_published': '2020',
           'latest': True,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 10030,
           'criteria': 'A2bd',
           'url': 'https://www.iucnredlist.org/species/10030/495630',
           'taxon_scientific_name': 'Hexanchus griseus',
           'red_list_category_code': 'NT',
           'assessment_id': 495630,
           'code': '1',
           'code_type': 'use_trade',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]},
          ...
          ...
          {'assessment_date': '2010-05-12T01:00:00.000+01:00',
           'year_published': '2013',
           'latest': False,
           'possibly_extinct': False,
           'possibly_extinct_in_the_wild': False,
           'sis_taxon_id': 152285,
           'criteria': None,
           'url': 'https://www.iucnredlist.org/species/152285/618900',
           'taxon_scientific_name': 'Cylindropuntia alcahes',
           'red_list_category_code': 'LC',
           'assessment_id': 618900,
           'code': '1',
           'code_type': 'use_trade',
           'scopes': [{'description': {'en': 'Global'}, 'code': '1'}]}],
         'filters': {}}
        """
        endpoint = f"use_and_trade/{code}"
        params = self._filter_params(
            page=page,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )

        return self.get(endpoint, params=params)


class IucnRedListApiSession(requests.Session):
    """A simple [`requests.Session`][requests.Session] based class for an API session.

    Examples
    --------
    >>> import os
    >>> session = IucnRedListApiSession(os.environ['API_KEY'])
    >>> type(session)
    <class 'api.IucnRedListApiSession'>
    >>> assert session.api_key == os.environ['API_KEY']
    >>> assert session.headers == {'Accept': 'application/json', 'Authorization': os.environ['API_KEY']}
    """

    _api_key: str

    def __init__(self, api_key: str) -> None:
        """Initialiser requiring the API username and key.

        Parameters
        ----------
        api_key : str
            The API key obtained from the registration profile on the API
            developer portal:

            https://api.iucnredlist.org/

        Examples
        --------
        >>> import os
        >>> session = IucnRedListApiSession(os.environ['API_KEY'])
        >>> assert session.api_key == os.environ['API_KEY']
        >>> assert session.headers == {'Accept': 'application/json', 'Authorization': os.environ['API_KEY']}
        """
        super().__init__()

        self._api_key = api_key
        self.headers = {"Accept": "application/json", "Authorization": self._api_key}

    @property
    def api_key(self) -> str:
        """The API key (obtained from the API developer portal profile).

        Returns
        -------
        str
            The API key.

        Examples
        --------
        >>> import os
        >>> session = IucnRedListApiSession(os.environ['API_KEY'])
        >>> assert session.api_key == os.environ['API_KEY']
        """
        return self._api_key


class IucnRedListApiResponse(requests.models.Response):
    """A simple [`requests.models.Response`][requests.models.Response] based wrapper for the API responses.

    Examples
    --------
    >>> import os
    >>> client = IucnRedListApiClient(os.environ['API_KEY'])

    """

    __attrs__ = Response.__attrs__

    def __init__(self, response: requests.Response) -> None:
        """Initialiser requiring a [requests.Response][] object.

        Parameters
        ----------
        response : requests.Response
            The response from the original request.
        """
        self.__dict__.update(**response.__dict__)

    @property
    def json(self) -> dict:
        """The API response data as JSON, if such data exists.

        Returns
        -------
        dict
            The data in the API response as JSON, if this exists. No data
            produces empty JSON.
        """
        try:
            return super().json()
        except (AttributeError, json.JSONDecodeError):
            return {}


if __name__ == "__main__":  # pragma: no cover
    # Doctest the module from the project root using
    #
    #     PYTHONPATH=src API_KEY="<API key>" python3 -m doctest -v src/iucn_redlist_api/api.py
    #
    # where "<API key>" must be replaced with an actual working Red List API
    # key for the relevant API version.
    import doctest

    doctest.testmod()
