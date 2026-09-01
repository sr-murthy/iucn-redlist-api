SHELL := /bin/bash

REPO := https://github.com/sr-murthy/iucn-redlist-api

PACKAGE_NAME := iucn-redlist-api
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
HEAD := $(shell git rev-parse --short=8 HEAD)
PACKAGE_VERSION := $(shell grep __version__ src/iucn_redlist_api/__init__.py | cut -d '=' -f 2 | xargs)

PROJECT_ROOT := $(PWD)

TESTS_ROOT := $(PROJECT_ROOT)/tests

#DOCS_ROOT := $(PROJECT_ROOT)/docs
#DOCS_BUILD := $(DOCS_ROOT)/_build
#DOCS_BUILD_HTML := $(DOCS_ROOT)/_build/html

# Make everything (possible)
all:

# Git
git_stage:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Staging new, modified, deleted and/or renamed files in Git\n"
	git status -uno | grep modified | tr -s ' ' | cut -d ' ' -f 2 | xargs git add && \
	git status -uno | grep deleted | tr -s ' ' | cut -d ' ' -f 2 | xargs git add -A && \
	git status -uno

# Housekeeping
clean:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Deleting all temporary files\n"
	rm -fr docs/_build/* .pytest_cache *.pyc *__pycache__* ./dist/* ./build/* *.egg-info*

# A simple version check for the installed package (local, sdist or wheel)
version_check:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Checking installed package version (if it is installed)\n"
	python3 -c "import os; os.chdir('src/iucn_redlist_api'); from __init__ import __version__; print(__version__); os.chdir('../')"

version_extract:
	echo "$(PACKAGE_VERSION)"

# Dependency management
sync_deps_exact:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Syncing all package + development dependencies, exactly in line with the UV lockfile\n"
	rm -f uv.lock && \
	uv sync --verbose --active --all-groups --no-install-project --no-cache --refresh --exact

sync_deps_inexact:
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Syncing all package + development dependencies, preserving pre-existing dependencies\n"
	rm -f uv.lock && \
	uv sync --verbose --active --all-groups --no-install-project --no-cache --refresh --inexact

# Pre-commit
pre-commit: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running pre-commit hooks\n"
	pre-commit run --all-files

# Running tests (NOTE: all tests require the API_KEY environment variable)
doctests: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running doctests in all core libraries\n"
	PYTHONPATH="src" uv run --active python3 -m doctest -v src/iucn_redlist_api/*.py

unittests: clean
	@echo "\n$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running package unit tests + measuring coverage\n"
	PYTHONPATH="src" uv run --active python3 -m pytest \
						                         --cache-clear \
							                     --capture=no \
							                     --code-highlight=yes \
							                     --color=yes \
							                     --cov=src \
							                     --cov-report=term-missing:skip-covered \
							                     -ra \
							                     --tb=native \
							                     --verbosity=3 \
							                    tests/units
