FROM python:3.4

RUN mkdir /code
WORKDIR /code

ADD . /code/
RUN pip install -r requirements.txt
RUN	python manage.py makemigrations && \
	python manage.py migrate && \
	python manage.py seed blogs --number=10
