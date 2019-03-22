FROM python:3.7-alpine

MAINTAINER faq@cryptic-game.net

ENV CROSS_ORIGIN True
ENV DEBUG False

WORKDIR /app

COPY ./app

RUN apk add gcc musl-dev libffi-dev libressl-dev

RUN pip install pipenv
RUN pipenv run pip install pip==18.0
RUN pipenv install

CMD pipenv run prod
