ENV_NAME = "venv"
DEPENDENCIES_FILE_NAME = "requirements.txt"

default: run

build: 
	poetry config warnings.export false
	poetry export --without-hashes -f $(DEPENDENCIES_FILE_NAME) -o $(DEPENDENCIES_FILE_NAME)
	python3 -m venv $(ENV_NAME)

prepare: 
	python3 -m pip install --user pipx
	python3 -m pipx ensurepath
	pipx install poetry
	make buildmake 
	make activate

activate: 
	. $(ENV_NAME)/bin/activate

u.poetry: pipx upgrade poetry

run: r
r:
	make activate
	python3 main.py

install: i
i:
	make activate
	pip install --no-cache-dir -r $(DEPENDENCIES_FILE_NAME)
