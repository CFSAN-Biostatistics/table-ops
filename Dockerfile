FROM python:3.10-slim-bullseye

COPY . /tools
WORKDIR /tools

ENTRYPOINT ["python", "table-union.py"]