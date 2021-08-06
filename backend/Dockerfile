FROM ubuntu:latest

USER root

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# install system dependencies
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  #&& apt-get -y install netcat gcc postgresql \ comente esta linea a ver qlq
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
# install python dependencies
#RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt
COPY . /backend
