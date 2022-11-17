FROM python:3.7-alpine

COPY . /tools
WORKDIR /tools

ENTRYPOINT ["python", "table-union.py"]