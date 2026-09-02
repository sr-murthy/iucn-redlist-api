# Getting Started

The requirements and installation process are fairly simple, and are described below in more detail.

## Requirements

* A minimum of Python 3.12+ is recommended, although Python 3.11 should also be generally fine on most platforms.

* You will also need to obtain an API key by registering an account linked to an accessible email on the <a href="https://api.iucnredlist.org/" target="_new">API portal</a>. Note that the Red List API restricts access for commercial use, and for any non-commercial user the best option is to indicate non-commercial use while registering. Then, make sure make the API key is available in the working environment either by exporting it with an environment variable, for example, `API_KEY`, or within the working Python interpreter using [`os.environ`](https://docs.python.org/3/library/os.html#os.environ).

## Installation / Setup

There is currently no public Python `iucn-redlist-api` package, so for the moment the best starting point is a clone of the [original repository](https://github.com/sr-murthy/iucn-redlist-api), or a clone of your own GitHub fork of the original.

From the cloned repository there are several options for using it as an importable package/library.

### Non-Editable Installation

Install the project as a regular library, from the project root, with either `pip`:

```shell
python3 -m pip install .
```
or with `uv`:

```shell
uv run --verbose --active pip install .
```

Now import `iucn_redlist_api` in a Python shell of your choice, and instantiate the client with the API key:

```shell
>>> import os; from iucn_redlist_api.api import *
>>> client = api.IucnRedListApiClient(os.environ['API_KEY'])
>>> client
IucnRedListApiClient(api_version="v4")
>>> client.api_version
{'api_version': 'v4'}
>>> client.get_information_red_list_version()
{'red_list_version': '2026-1'}
```

All Red List API requests are handled via the [`IucnRedListApiSession`][iucn_redlist_api.api.IucnRedListApiSession] object on the client, and all requests are `GET` requests. All responses are [`IucnRedListApiResponse`][iucn_redlist_api.api.IucnRedListApiResponse] objects, with response data available in JSON from the [`json`][iucn_redlist_api.api.IucnRedListApiResponse.json] attribute. Consult the [API Reference][api-client-reference] for more information.

In both cases, all package dependencies (at the moment, just the [`requests`][requests] library) and development dependencies, as defined in the [project TOML](https://github.com/sr-murthy/iucn-redlist-api/blob/main/pyproject.toml), will be installed into the working environment **in addition to** the project itself, which will also be installed as an importable library, `iucn_redlist_api`.

!!! note
    `uv` by default installs and manages all dependencies in a hidden subfolder named `.venv` located in the working directory where it was installed. This may cause problems if you already have a different (e.g. pre-existing or working) environment you wish to use: in this case, either export the path to the preferred environment via the [`UV_PROJECT_ENVIRONMENT`](https://docs.astral.sh/uv/reference/environment/#uv_project_environment) environment variable, or use the `--active` flag to target the active environment.

### Editable Installation

If you're interested in evaluating or contributing to the project, you can install the project in editable (or development) mode - once again from the project root - with either [`pip`](https://pip.pypa.io/en/):
```shell
python3 -m pip install -e .
```
or [Astral `uv`](https://docs.astral.sh/uv/):
```shell
uv sync --active --verbose --all-groups --no-cache --refresh --inexact
```

Now import the library in exactly the same way as with the non-editable installation option above.

In the editable installation local changes to the source files (in `src/iucn_redlist_api/`) are reflected in the installed library functionality. This is the best option if you wish to contribute to the project via pull requests.

### Direct Use from Source

You can also use the client library directly from source in a Python interpreter, with only the project dependencies - not the project itself - installed into the working environment, for example, with `uv` using a variant of the command above with the addition of the `--no-install-project` flag, e.g.:
```shell
uv sync --active --verbose --all-groups --no-install-project --no-cache --refresh --inexact
```
Accessing the client works exactly the same way as described above, except that it requires a preliminary step to set the Python path to the main package:
```shell
>>> import sys; sys.path.insert(0, 'src')
>>> import importlib, os; import iucn_redlist_api.api; importlib.reload(iucn_redlist_api.api); from iucn_redlist_api.api import *
>>> client = api.IucnRedListApiClient(os.environ['API_KEY'])
>>> client
IucnRedListApiClient(api_version="v4")
```

## Using the API Client

There is a comprehensive [Red List API reference](https://api.iucnredlist.org/api-docs/index.html) that can be consulted to understand the API itself, and the `iucn-redlist-api` is a very thin client around this API, with a public method for every API endpoint. The API client methods are fully documented in the [API client reference](api-client-reference), with example snippets.

A more detailed client usage guide will be added at some point in the future.
