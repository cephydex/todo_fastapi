FROM python:3.10.8-slim

RUN apt-get update && apt-get install -y libpq-dev \
    postgresql \
    python-dev 

WORKDIR /app

# env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt

COPY . .
# WORKDIR /app