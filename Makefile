.PHONY: help test server unit functional

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

run:
	screen -S server python manage.py runserver
    # C-a a d
    # screen -rd server

test: ut ft

ut:
	@clear
	python manage.py test blog
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
