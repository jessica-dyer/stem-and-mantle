all: lint test

setup:
	poetry install --with dev
	poetry export -f requirements.txt --output requirements.txt --without-hashes

lint: setup
	poetry run black .
	poetry run ruff . --fix

test: setup
	# poetry run pytest tests/unit

run: setup 
	poetry run uvicorn main:app --reload