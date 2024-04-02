ENV_NAME = "venv"
DEPENDENCIES_FILE_NAME = "requirements.txt"

default: run

build:
	poetry config warnings.export false
	poetry export --without-hashes -f $(DEPENDENCIES_FILE_NAME) -o $(DEPENDENCIES_FILE_NAME)
	python3 -m venv $(ENV_NAME)

prepare: 
	rm -rf ./requirements.txt
	rm -rf ./venv
	python3 -m pip install --user pipx
	python3 -m pipx ensurepath --force
	pipx install poetry --force
	make build
	make activate

activate:
	source $(ENV_NAME)/bin/activate

deactivate:
	source $(ENV_NAME)/bin/deactivate

u.poetry: pipx upgrade poetry

run: r
r:
	python3 api.py

install: i
i:
	poetry config warnings.export false
	poetry export --without-hashes -f $(DEPENDENCIES_FILE_NAME) -o $(DEPENDENCIES_FILE_NAME)
	pip install --no-cache-dir -r $(DEPENDENCIES_FILE_NAME)

f:
	pip freeze >> requirements.txt
