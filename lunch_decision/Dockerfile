# Final image.
FROM python:3.9.12-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential=12.6 \
  git=1:2.20.* \
  libpq-dev=* \
  curl=* \
  libcurl4-openssl-dev=* \
  libssl-dev=* \
  libssl1.1 \
  unzip=* \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /lunch_decision
COPY requirements.txt /lunch_decision/
RUN pip install -r requirements.txt
COPY . /lunch_decision/

#ENV DATABASE_URL=postgres://myprojectuser:pass123456A@db:5432/postgresdb

