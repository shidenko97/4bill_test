FROM python:3.8.1

MAINTAINER Serhii Hidenko "shidenko97@gmail.com"

RUN mkdir -p /var/www/flask-app
WORKDIR /var/www/flask-app

ADD requirements.txt /var/www/flask-app/
RUN pip install -r requirements.txt

ADD . /var/www/flask-app