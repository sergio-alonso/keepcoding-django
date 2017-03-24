.PHONY: help run test ut ft db db_clean static seed coverage

default: help

help:
	@echo "help - Show this help"
	@echo "run - Start development server"
	@echo "test - Run all tests"
	@echo "ut - Run unit tests"
	@echo "ft - Run functional tests"
	@echo "bd - Handle databse"
	@echo "db_clean - Recreate a fresh database"
	@echo "static - Handle static files"
	@echo "seeEd - Populate with dummy data"
	@echo "coverage - Code coverage"

run:
	screen -S server python manage.py runserver
    # C-a a d
    # screen -rd server

test:
	python manage.py test --parallel -v0

coverage:
	coverage run --source='.' manage.py test functional_tests blogs accounts blogs -v0
	coverage report

ut:
	@clear
	python manage.py test blogs
	python manage.py test accounts

ft:
	@clear
	python manage.py test functional_tests

db:
	python manage.py makemigrations
	python manage.py migrate

db_clean:
	rm db.sqlite3
	python manage.py migrate --noinput

static:
	python manage.py collectstatic

seed:
	python manage.py seed blogs --number=10
