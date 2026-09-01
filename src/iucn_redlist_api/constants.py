__all__ = [
    "IUCN_RED_LIST_API_CONSTANTS",
]


# -- IMPORTS --

# -- Standard libraries --
from enum import Enum

# -- 3rd party libraries --

# -- Internal libraries --


class IUCN_RED_LIST_API_CONSTANTS(Enum):
    """An enum of useful API information.

    Examples
    --------
    >>> IUCN_RED_LIST_API_CONSTANTS.DEVELOPER_PORTAL.value
    'https://api.iucnredlist.org'
    >>> IUCN_RED_LIST_API_CONSTANTS.API_VERSION.value
    'v4'
    >>> IUCN_RED_LIST_API_CONSTANTS.API_REFERENCE.value
    'https://api.iucnredlist.org/api-docs/index.html'
    >>> IUCN_RED_LIST_API_CONSTANTS.BASEURL.value
    'https://api.iucnredlist.org/api/v4'
    """

    DEVELOPER_PORTAL = "https://api.iucnredlist.org"

    API_VERSION = "v4"

    API_REFERENCE = "https://api.iucnredlist.org/api-docs/index.html"

    BASEURL = f"{DEVELOPER_PORTAL}/api/{API_VERSION}"
