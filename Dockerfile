FROM python:3.4
MAINTAINER Sergio Alonso <sergio@sergioalonso.es>

VOLUME ["/code"]
WORKDIR "/code"

COPY requirements.txt /code

RUN pip install --requirement requirements.txt

COPY . /code/
