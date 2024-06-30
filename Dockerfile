FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY skymarket/.env ./skymarket/

COPY . .