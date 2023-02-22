FROM python:3.9-slim-buster

WORKDIR /api

COPY ./app/requirements.txt ./api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./api/requirements.txt

COPY ./app /api/
