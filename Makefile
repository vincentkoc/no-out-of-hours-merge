.PHONY: help lint format test coverage install-requirements install-venv update-pip-requirements clean precommit update-precommit
.DEFAULT_GOAL := help

# Setup ENV
SHELL := /bin/bash
include .env
export

# Setup additional variables
TAG := $(shell git describe --tags --always --dirty)
BLUE=\033[0;34m
ORANGE=\033[1;33m
NC=\033[0m # No Color
UNAME := $(shell uname)

# Check for Virtualenv
# RUNNING_INSIDE_VENV = 1 if running inside the virtual environment
# RUNNING_OUTSIDE_VENV = 1 if running outside the virtual environment
# VENV_NOT_INSTALLED = 1 if the virtual environment is not installed
RUNNING_INSIDE_VENV := $(shell [ -n "$$VIRTUAL_ENV" ] && echo 1 || echo 0)
RUNNING_OUTSIDE_VENV := $(shell [ -n "$$VIRTUAL_ENV" ] && echo 0 || echo 1)
VENV_NOT_INSTALLED := $(if $(shell [ -d "$(VENV)" ] || echo not_installed), 0, 1)

ifeq ($(RUNNING_INSIDE_VENV),1)
CHECKVENV := 2
PYTHON := "./$(VENV)/bin/python3"
PIP := "./$(VENV)/bin/pip3"
else
CHECKVENV := $(if $(VENV_NOT_INSTALLED), 0, 1)
endif

# Display help information
help:
	@echo -e "$(BLUE)----------------------------------------"
	@echo -e "Automated makefile helper for: $(APPNAME)"
	@echo -e "----------------------------------------$(NC)"
	@echo
	@echo "Makefile commands:"
	@echo
	@echo "  install-requirements"
	@echo "  install-venv"
	@echo "  update-pip-requirements"
	@echo "  update-precommit"
	@echo "  lint"
	@echo "  format"
	@echo "  test"
	@echo "  coverage"
	@echo "  clean"
	@echo "  precommit"
	@echo "  help"
	@echo

# Lint code
lint:
	@echo "🚜 Linting code with flake8..."
	$(PYTHON) -m flake8 src/ --count

# Format code
format:
	@echo "🚜 Formatting code with black..."
	$(PYTHON) -m black src/

# Run unit tests
test:
	@echo "🧪 Running unit tests..."
	$(PYTHON) -m unittest discover -t ./src/ -s ./src/tests

# Run unit tests with coverage
coverage:
	@echo "🧪 Running unit tests and generating coverage..."
	$(PYTHON) -m coverage erase
	$(PYTHON) -m coverage run --source="./src/" -m unittest discover -t ./src/ -s ./src/tests
	$(PYTHON) -m coverage html

# Install requirements
install-requirements:
	@if [ "$(RUNNING_OUTSIDE_VENV)" = "1" ]; then \
		echo "🚨 You are not running inside a virtual environment. Please run 'make install-venv' first." && exit 1; \
	fi
	@echo "✨ Upgrading pip ($(PIP))..."
	$(PYTHON) -m pip install --upgrade $(PY_PIP_EXTRAS)
	@echo "✨ Installing dev requirements using pip ($(PIP))..."
	$(PIP) install -r requirements-dev.txt
	@echo "✨ Installing pre-commit hooks..."
	pre-commit install

# Create and activate a virtual environment
install-venv:
	@echo "✨ Installing Virtualenv..."
	$(PYTHON) -m venv $(VENV)
	@echo "✨ Run the following command to activate the virtual environment:"
	@echo "source $(VENV)/bin/activate"

# Clean generated files
clean:
	@echo "✨ Cleaning all cache, coverage and venv..."
	rm -rf .venv coverage/* .pytest_cache/ .mypy_cache/ .coverage

# Run prec-commit hooks
precommit:
	@echo "🛫 Running pre-commit hooks..."
	pre-commit run --all-files

# Update pre-coomit hooks
update-precommit:
	@echo "🛫 Updating pre-commit hooks..."
	pre-commit autoupdate
