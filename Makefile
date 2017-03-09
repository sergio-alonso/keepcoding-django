all: test

server:
	python manage.py runserver

test:
	python functional_test.py
