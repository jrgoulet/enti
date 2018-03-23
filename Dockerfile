FROM python:3.6-slim
MAINTAINER Joe Goulet <joseph.goulet@digitalreasoning.com>

COPY ./requirements.txt /opt/entity-manager/
WORKDIR /opt/entity-manager

RUN apt-get update && apt-get install -y python3-dev gcc libmysqlclient-dev
RUN pip install -r /opt/entity-manager/requirements.txt
RUN apt-get -o Dpkg::Options::="--force-confmiss" install -y --reinstall netbase

COPY . /opt/entity-manager

CMD gunicorn -k eventlet -w 1 manager:app -b ${SERVER_HOST}:${SERVER_PORT}