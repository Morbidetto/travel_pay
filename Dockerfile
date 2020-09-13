FROM python:3-slim

RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


COPY . .
EXPOSE 8000
