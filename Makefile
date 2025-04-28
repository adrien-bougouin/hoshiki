.DEFAULT_GOAL := run

module := hoshiki

python := pipenv run python
pylint := pipenv -q run pylint
flake8 := pipenv -q run flake8
mypy := pipenv -q run mypy

Pipenv.lock: Pipfile
	pipenv lock

dependencies: Pipenv.lock
	pipenv sync
	pipenv sync --dev
.PHONY: dependencies

check: type-check style-check
.PHONY: check

style-check:
	$(pylint) $(module) --score n $(PYLINT_ARGS)
	$(flake8) $(module)
.PHONY: style-check

type-check:
	$(mypy) $(module) --strict --warn-redundant-casts
.PHONY: type-check

run:
	$(python) -m $(module) $(ARGS)
.PHONY: run

run-help:
	$(python) -m $(module) --help
.PHONY: run-help

clean:
	rm -rf $(module)/__pycache__
	rm -rf $(module)/**/__pycache__
	rm -rf .mypy_cache
.PHONY: clean

clean-venv:
	pipenv --rm
.PHONY: clean
