FROM python:3.10-slim

RUN mkdir /app && mkdir /app/media && mkdir /app/src

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.in-project true \
    && poetry install --without dev,test --no-interaction --no-ansi

COPY src /app/src

WORKDIR /app

