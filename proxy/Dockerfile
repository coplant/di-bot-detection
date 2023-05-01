FROM python:3-slim-buster

WORKDIR /code/proxy

COPY /requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /code/proxy/docker/*.sh