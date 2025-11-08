# Makefile — MyST site helpers for Datahub
# Usage:
#   make env                # create or update the conda env (no activation)
#   make html               # build local HTML (_build/html)
#   make clean              # remove figures/, audio/, _build/

SHELL := /bin/bash

# You can override these at call time, e.g.:
#   make ENV_NAME=myenv env
#   make MYST_CMD="npx mystmd" html
ENV_NAME ?= myst-env
# On Datahub, it's easiest to use myst via npx (no install):
MYST_CMD ?= npx mystmd

.PHONY: env html clean help

env:
	@set -euo pipefail ; \
	if ! command -v conda >/dev/null 2>&1 ; then \
		echo "ERROR: conda not found on this image."; exit 1 ; \
	fi ; \
	if [ ! -f environment.yml ]; then \
		echo "ERROR: environment.yml not found in repo root." ; exit 1 ; \
	fi ; \
	# If the env exists, update it; otherwise create it
	if conda env list | awk '{print $$1}' | grep -qx "$(ENV_NAME)"; then \
		echo "Updating existing env '$(ENV_NAME)' from environment.yml..." ; \
		conda env update -n "$(ENV_NAME)" -f environment.yml --prune ; \
	else \
		echo "Creating env '$(ENV_NAME)' from environment.yml..." ; \
		conda env create -n "$(ENV_NAME)" -f environment.yml ; \
	fi ; \
	echo "Done. (Not activating; on Datahub you generally don't need to for 'make html')"

html:
	@set -euo pipefail ; \
	echo "Building local HTML with $(MYST_CMD)..." ; \
	$(MYST_CMD) build --html ; \
	echo "Build complete. Open _build/html/index.html in the file browser."

clean:
	@set -euo pipefail ; \
	echo "Removing figures/, audio/, and _build/ ..." ; \
	rm -rf figures audio _build ; \
	echo "Clean complete."

help:
	@echo "Targets:"
	@echo "  make env    - create/update conda env from environment.yml (no activation)"
	@echo "  make html   - build local HTML (runs: $(MYST_CMD) build --html)"
	@echo "  make clean  - remove figures/, audio/, and _build/"
