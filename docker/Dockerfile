FROM python:3.6.9-slim-stretch
LABEL maintainer="Amit Chavhan <amitc005@gmail.com>"

RUN apt-get update && apt-get install -y vim make wget python-dev build-essential

EXPOSE 8000

RUN mkdir /usr/local/team_monitor/
WORKDIR /usr/local/team_monitor/

COPY requirements.txt /usr/local/team_monitor/
RUN pip install -r requirements.txt
