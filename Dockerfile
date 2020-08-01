FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code/
WORKDIR /code

RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev build-base linux-headers && \
  apk add --no-cache jpeg-dev zlib-dev && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

ENV \
  DEBUG=1 \
  SECRET_KEY=foo \
  DB_NAME=foodsquare \
  DB_USER=postgres \
  DB_PASS=postgres \
  DB_HOST=db \
  DB_PORT=5432
