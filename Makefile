.PHONY: help test server unit

default: help

help:
	@echo "help - Show this help"
	@echo "run - Start development server"
	@echo "test - Run functional tests"
	@ech0 "unit - Run unit tests"

run:
	python manage.py runserver

test:
	python functional_test.py

unit:
	python manage.py test
