FROM python:3.9.2-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --dev --deploy --system

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
