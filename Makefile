.PHONY: help test server unit functional

default: help

help:
	@echo "help - Show this help"
	@echo "run - Start development server"
	@echo "test - Run all tests"
	@echo "unit - Run unit tests"
	@echo "functional - Run functional tests"

run:
	screen -S server python manage.py runserver
    # C-a a d
    # screen -rd server

test: unit functional

unit:
	python manage.py test

functional: ft_anonymous ft_user

ft_anonymous:
	python ft_anonymous.py

ft_user:
	python ft_user.py
