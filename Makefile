.PHONY: help test server unit functional

default: help

help:
	@echo "help - Show this help"
	@echo "run - Start development server"
	@echo "test - Run all tests"
	@echo "unit - Run unit tests"
	@echo "functional - Run functional tests"

run:
	python manage.py runserver

test: unit functional

unit:
	python manage.py test

functional:
	python ft_anonymous.py
