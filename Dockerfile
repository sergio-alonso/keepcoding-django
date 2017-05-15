FROM python:3.4

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt && \
	python manage.py makemigrations && \
	python manage.py migrate && \
	python manage.py seed blogs --number=10

ADD . /code/
