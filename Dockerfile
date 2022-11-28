FROM python:3.7-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache bash

COPY . /tools
WORKDIR /tools

ENTRYPOINT ["python", "table-union.py"]