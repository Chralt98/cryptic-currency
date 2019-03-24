FROM python:3.7-alpine

MAINTAINER faq@cryptic-game.net

ENV CROSS_ORIGIN True
ENV DEBUG False

WORKDIR /app

ADD . /app/

RUN apt-get install python3-dev default-libmysqlclient-dev
RUN apk add gcc musl-dev libffi-dev libressl-dev

RUN pip install pipenv
RUN pipenv run pip install pip==18.0
RUN pipenv install

CMD pipenv run prod
