FROM python:3.6-slim
MAINTAINER Joe Goulet <joseph.goulet@digitalreasoning.com>

COPY ./requirements.txt /opt/enti/
WORKDIR /opt/enti

RUN apt-get update && apt-get install -y python3-dev gcc libmysqlclient-dev
RUN pip install -r /opt/enti/requirements.txt
RUN apt-get -o Dpkg::Options::="--force-confmiss" install -y --reinstall netbase

COPY . /opt/enti

CMD gunicorn -k eventlet -w 1 enti:app -b ${SERVER_HOST}:${SERVER_PORT}