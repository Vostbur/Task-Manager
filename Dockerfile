FROM python:3.9.2-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update

# install psycopg2 dependencies
RUN apk add --no-cache \
        postgresql-dev \
        gcc \
        python3-dev \
        musl-dev

# install cryptography dependencies
RUN apk add --no-cache \
        libressl-dev \
        libffi-dev \
        openssl-dev \
        cargo

RUN pip install --upgrade pip

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --dev --deploy --system

COPY . .
