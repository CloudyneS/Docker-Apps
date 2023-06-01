FROM unit:python3.11

LABEL Version="1.0"
LABEL Maintainer="Cloudyne Systems"
LABEL org.opencontainers.image.source="https://github.com/cloudynes/docker-apps"
LABEL Description="Django and Nginx Unit container for Kubernetes deployment"
LABEL org.opencontainers.image.description="Django and Nginx Unit container for Kubernetes deployment"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

RUN cd /app && python3 -m venv .venv && . .venv/bin/activate && pip3 install Django && django-admin startproject djtest .

ADD config.json /docker-entrypoint.d/config.json

EXPOSE 8123