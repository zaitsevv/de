VENV=./venv
ENV=./.env
REQUIREMENTS=./requirements.txt
ROOMS_PATH=./data/rooms.json
STUDENTS_PATH=./data/students.json
OUTPUT_PATH=.
OUTPUT_FORMAT=json

create_virtual_env:
	python -m venv $(VENV) && \
	. $(VENV)/bin/activate && \
	. $(ENV) && \
	pip install -r $(REQUIREMENTS) && \
	pre-commit install

run_tests:
	. $(VENV)/bin/activate && pytest

run_postgresql:
	docker compose up -d

stop_postgresql:
	docker compose down

build:
	make create_virtual_env
	make run_tests
	make run_postgresql

default_run:
	. $(VENV)/bin/activate && \
 	. $(ENV) && \
 	python src/main.py --rooms-path $(ROOMS_PATH) \
 					   --students-path $(STUDENTS_PATH) \
 					   --output-path $(OUTPUT_PATH) \
 					   --output-format $(OUTPUT_FORMAT)

stop_services:
	make stop_postgresql
