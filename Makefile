all: run

run:
	poetry run uvicorn coalesce_api.api:app

test:
	poetry run python -m pytest --cov=coalesce_api --cov-context=test --cov-report=html -vv --showlocals $(args)

init:
	poetry install
	poetry run pre-commit install

.PHONY: all run test init
