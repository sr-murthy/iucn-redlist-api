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
    IucnRedListApiClient(api_version="v4")
    >>> assert client.api_session.api_key == os.environ['API_KEY']
    >>> client.get("information/api_version").json
    {'api_version': 'v4'}
    >>> client.get("information/red_list_version").json
    {'red_list_version': '2026-1'}

    Get biogeographical realms.

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

    Get kingdom taxa.

    >>> client.get_taxa_kingdom().json
    {'kingdom_names': ['ANIMALIA', 'CHROMISTA', 'FUNGI', 'PLANTAE']}

    Get the latest data and assessments for the Tawny Eagle (Aquila rapax).

    >>> data = client.get_taxa_scientific_name_assessments('Aquila', 'rapax').json
    >>> data['taxon']  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    {'sis_id': 22696033,
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
     'ssc_groups': [{'name': 'IUCN SSC Bird Red List Authority (BirdLife International)',
       'url': 'https://datazone.birdlife.org/',
       'description': 'Red List Authority Coordinator: Ian Burfield (ian.burfield@birdlife.org)'}],
     'common_names': [{'main': False, 'name': 'Águila Rapaz', 'language': 'spa'},
      {'main': False, 'name': 'Aigle ravisseur', 'language': 'fre'},
      {'main': True, 'name': 'Tawny Eagle', 'language': 'eng'}],
     'synonyms': [{'name': 'Falco rapax Temminck, 1828',
       'status': 'ACCEPTED',
       'genus_name': 'Falco',
       'species_name': 'rapax',
       'species_author': 'Temminck, 1828',
       'infrarank_author': None,
       'subpopulation_name': None,
       'infra_type': None,
       'infra_name': None}]}
    """

    # All instances have thse private attributes
    _api_session: IucnRedListApiSession
    _debug_mode: bool = False

    def _set_up_logger(self) -> None:
        """Sets up the API client logger with a console handler.

        This is only called if the client is called with ``debug_mode`` set
        to ``True``.

        No file handlers are set.
        """
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        self._logger = logging.getLogger(__name__)
        if not self._logger.handlers:
            logging.basicConfig(
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                level=logging.DEBUG,
                stream=sys.stdout,
            )

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
        IucnRedListApiClient(api_version="v4")
        >>> assert client.api_session.api_key == os.environ['API_KEY']
        >>> assert client.api_session.headers == {'Accept': 'application/json', 'Authorization': os.environ['API_KEY']}
        >>> client.api_version
        'v4'
        """
        self._api_session = IucnRedListApiSession(api_key)

        if debug_mode:
            self._debug_mode = debug_mode
            self._set_up_logger()

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
        return f'IucnRedListApiClient(api_version="{self.api_version}")'

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
        >>> assert 'error' not in client.get_assessment(259841783).json
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
        >>> assert 'error' not in client.assessment_search(filter_on=['eu_27_post_2020_endemic']).json
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
        >>> assert 'error' not in client.get_biogeographical_realms().json
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
        >>> assert 'error' not in client.get_biogeographical_realm_assessments('1', page=1).json
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
        >>> assert 'error' not in client.get_comprehensive_groups().json
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
        >>> assert 'error' not in client.get_comprehensive_group_assessments('amphibians', page=1).json
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
        >>> assert 'error' not in client.get_conservation_actions().json
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
        >>> assert 'error' not in client.get_conservation_action_assessments('1', page=1).json
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
        >>> assert 'error' not in client.get_countries().json
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
        >>> assert 'error' not in client.get_country_assessments('AD', page=1).json
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
        >>> assert 'error' not in client.get_faos().json
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
        >>> assert 'error' not in client.get_fao_assessments('18', page=1).json
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
        >>> assert 'error' not in client.get_growth_forms().json
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
        >>> assert 'error' not in client.get_growth_form_assessments('A', page=1).json
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
        >>> assert 'error' not in client.get_green_status_all().json
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
        >>> assert 'error' not in client.get_habitats().json
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
        >>> assert 'error' not in client.get_habitat_assessments('1', page=1).json
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
        >>> client.get_population_trends().json
        {'population_trends': [{'description': {'en': 'Increasing'}, 'code': '0'}, {'description': {'en': 'Decreasing'}, 'code': '1'}, {'description': {'en': 'Stable'}, 'code': '2'}, {'description': {'en': 'Unknown'}, 'code': '3'}]}
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
        >>> assert 'error' not in client.get_habitat_assessments('1', page=1).json
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
        >>> assert 'error' not in client.get_red_list_categories().json
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
        >>> assert 'error' not in client.get_red_list_category_assessments('A', page=1).json
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
        >>> assert 'error' not in client.get_research().json
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
        >>> assert 'error' not in client.get_red_list_category_assessments('A', page=1).json
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
        >>> assert 'error' not in client.get_scopes().json
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
        >>> assert 'error' not in client.get_scope_assessments('1', page=1).json
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
        >>> assert 'error' not in client.get_statistics_count().json
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
        >>> assert 'error' not in client.get_stresses().json
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
        >>> assert 'error' not in client.get_stress_assessments('1', page=1).json
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
        >>> assert 'error' not in client.get_systems().json
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
        >>> assert 'error' not in client.get_system_assessments('1', page=1).json
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
        >>> assert 'error' not in client.get_taxa_sis_assessments(158189).json # doctest: +NORMALIZE_WHITESPACE
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
        >>> assert 'error' not in client.get_taxa_scientific_name_assessments('Aquila', 'rapax').json # doctest: +NORMALIZE_WHITESPACE
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
        >>> client.get_taxa_kingdom().json
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
        >>> assert 'error' not in client.get_taxa_kingdom_assessments('Animalia', page=1).json # doctest: +NORMALIZE_WHITESPACE
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
        >>> res = client.get_taxa_phylum()
        >>> res.json['phylum_names'][:10]
        ['ANNELIDA', 'ANTHOCEROTOPHYTA', 'ARTHROPODA', 'ASCOMYCOTA', 'BASIDIOMYCOTA', 'BRYOPHYTA', 'CHAROPHYTA', 'CHLOROPHYTA', 'CHORDATA', 'CNIDARIA']
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
        >>> assert 'error' not in client.get_taxa_phylum_assessments('Annelida', latest=True).json # doctest: +NORMALIZE_WHITESPACE
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
        >>> res = client.get_taxa_class().json
        >>> res['class_names'][:10]
        ['ACTINOPTERYGII', 'AGARICOMYCETES', 'AMPHIBIA', 'ANDREAEOPSIDA', 'ANTHOCEROTOPSIDA', 'ANTHOZOA', 'ARACHNIDA', 'ARTHONIOMYCETES', 'ASTEROIDEA', 'AVES']
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
        >>> assert 'error' not in client.get_taxa_class_assessments('Acarosporales', latest=True).json
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
        >>> res = client.get_taxa_order().json
        >>> res['order_names'][:10] # doctest: +NORMALIZE_WHITESPACE
        ['ACAROSPORALES', 'ACCIPITRIFORMES', 'ACIPENSERIFORMES', 'ACOCHLIDIIMORPHA', 'ACORALES', 'ACROCHAETIALES', 'ACTINIARIA', 'ADAPEDONTA', 'AFROSORICIDA', 'AGARICALES']
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
        >>> assert 'error' not in client.get_taxa_order_assessments('Acarosporales', latest=True).json # doctest: +NORMALIZE_WHITESPACE
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
        >>> res = client.get_taxa_family().json
        >>> res['family_names'][:10]
        ['ABROCOMIDAE', 'ACANTHACEAE', 'ACANTHAMETROPODIDAE', 'ACANTHISITTIDAE', 'ACANTHIZIDAE', 'ACANTHOCOCCIDAE', 'ACANTHODRILIDAE', 'ACANTHOGORGIIDAE', 'ACANTHURIDAE', 'ACAROSPORACEAE']
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
        >>> assert 'error' not in client.get_taxa_family_assessments('Abrocomidae', latest=True).json
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
        >>> assert 'error' not in client.get_taxa_possibly_extinct().json # doctest: +NORMALIZE_WHITESPACE
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
        >>> assert 'error' not in client.get_taxa_possibly_extinct_in_the_wild().json # doctest: +NORMALIZE_WHITESPACE
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
        >>> assert 'error' not in client.get_threats().json # doctest: +NORMALIZE_WHITESPACE
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
        >>> assert 'error' not in client.get_threat_assessments('1', page=1).json # doctest: +NORMALIZE_WHITESPACE
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
        >>> assert 'error' not in client.get_use_and_trade().json # doctest: +NORMALIZE_WHITESPACE
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
        >>> assert 'error' not in client.get_use_and_trade_assessments('1', page=1).json # doctest: +NORMALIZE_WHITESPACE
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
