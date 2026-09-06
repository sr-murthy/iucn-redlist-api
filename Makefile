SHELL := /bin/bash

REPO := https://github.com/sr-murthy/iucn-redlist-api

PACKAGE_NAME := iucn-redlist-api
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
HEAD := $(shell git rev-parse --short=8 HEAD)
PACKAGE_VERSION := $(shell grep __version__ src/iucn_redlist_api/__init__.py | cut -d '=' -f 2 | xargs)

PROJECT_ROOT := $(PWD)

TESTS_ROOT := $(PROJECT_ROOT)/tests

DOCS_ROOT := $(PROJECT_ROOT)/docs
DOCS_BUILD := $(PROJECT_ROOT)/site

# Git
git-stage:
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Staging new, modified, deleted and/or renamed files in Git"
	git status -uno | grep modified | tr -s ' ' | cut -d ' ' -f 2 | xargs git add && \
	git status -uno | grep deleted | tr -s ' ' | cut -d ' ' -f 2 | xargs git add -A && \
	git status -uno

# Housekeeping
.PHONY: clean
clean:
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Deleting all temporary files"
	rm -fr docs/_build/* .pytest_cache *.pyc *__pycache__* ./dist/* ./build/* *.egg-info*

# A simple version check for the installed package (local, sdist or wheel)
version-check:
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Checking installed package version (if it is installed)"
	python3 -c "import os; os.chdir('src/iucn_redlist_api'); from __init__ import __version__; print(__version__); os.chdir('../')"

version-extract:
	echo "$(PACKAGE_VERSION)"

# Dependency management
sync-deps-exact:
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Syncing all package + development dependencies, exactly in line with the UV lockfile"
	rm -f uv.lock && \
	uv sync --verbose --active --all-groups --no-install-project --no-cache --refresh

sync-deps-inexact:
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Syncing all package + development dependencies, preserving pre-existing dependencies"
	rm -f uv.lock && \
	uv sync --verbose --active --all-groups --no-install-project --no-cache --refresh --inexact

# --- Package artifacts ---
.PHONY: sdist
sdist: clean
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Building source distribution"
	uv run hatchling build --target sdist --clean
	tar tvf ./dist/*.tar.gz

.PHONY: wheel
wheel: clean
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Building wheel"
	uv run hatchling build --target wheel --clean
	tar tvf ./dist/*.whl

.PHONY: all
all: clean
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Building source distribution + wheel"
	uv run hatchling build --clean
	tar tvf ./dist/*.tar.gz
	tar tvf ./dist/*.whl

# Pre-commit
.PHONY: pre-commit
pre-commit: clean
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running pre-commit hooks"
	pre-commit run --all-files

# Doctests - requires API key (`API_KEY`) to be available in the environment
.PHONY: doctest
doctest: clean
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running doctests in all core libraries"
	PYTHONPATH="src" uv run --active python3 -m doctest -v src/iucn_redlist_api/*.py

# Unit tests
.PHONY: test
test: clean
	@echo "$(PACKAGE_NAME)[$(BRANCH)@$(HEAD)]: Running package unit tests + measuring coverage"
	PYTHONPATH="src" uv run --active pytest \
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
