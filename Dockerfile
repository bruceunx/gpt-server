FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY ./gpt_server /app/gpt_server

