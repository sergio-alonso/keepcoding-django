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

run:
	screen -S server python manage.py runserver
    # C-a a d
    # screen -rd server

test: ut ft

ut:
	@clear
	python manage.py test blog

ft:
	python manage.py test functional_tests

db:
	python manage.py makemigrations
	python manage.py migrate

db_clean:
	rm db.sqlite3
	python manage.py migrate --noinput
