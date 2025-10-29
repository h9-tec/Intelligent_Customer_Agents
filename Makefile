SHELL := /usr/bin/bash

.PHONY: setup run worker beat test seed lint

setup:
	python3 -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate

run:
	. .venv/bin/activate && export DJANGO_SETTINGS_MODULE=project_core.settings.dev && python manage.py runserver 0.0.0.0:8000

worker:
	. .venv/bin/activate && celery -A project_core.celery worker -l info

beat:
	. .venv/bin/activate && celery -A project_core.celery beat -l info

test:
	. .venv/bin/activate && pytest --cov=.

seed:
	. .venv/bin/activate && python manage.py seed_all

lint:
	. .venv/bin/activate && ruff check .


