__all__ = [
    "IucnRedListApiClientException",
    "IucnRedListApiException",
    "IucnRedListApiRequestException",
    "IucnRedListApiResponseException",
]


# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --


class IucnRedListApiException(Exception):
    """Base class for all API exceptions."""


class IucnRedListApiRequestException(IucnRedListApiException):
    """Base class all API request exceptions."""


class IucnRedListApiResponseException(IucnRedListApiException):
    """Base class all API response exceptions."""


class IucnRedListApiClientException(IucnRedListApiException):
    """Base class for an API client exceptions."""
