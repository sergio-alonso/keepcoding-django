.PHONY: help test server

default: help

help:
	@echo "help - Show this help"
	@echo "run - Start development server"
	@echo "test - Run tests"

run:
	python manage.py runserver

test:
	python functional_test.py
