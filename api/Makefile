all: lint test

setup:
	poetry install --with dev

lint: setup
	poetry run black .
	poetry run ruff . --fix

test: setup
	# poetry run pytest tests/unit