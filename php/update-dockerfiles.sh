#!/bin/bash
rm -rf /tmp/php-docker && \
git clone https://github.com/docker-library/php.git /tmp/php-docker && \
# ADD PHP7.4 HERE
cp -r /tmp/php-docker/8.0/alpine3.16/cli/* ./8.0/ && \
cp -r /tmp/php-docker/8.1/alpine3.17/cli/* ./8.1/ && \
cp -r /tmp/php-docker/8.2/alpine3.18/cli/* ./8.2/ && \

sed -i 's/--enable-option-checking=fatal/--enable-option-checking=fatal --enable-embed/' Dockerfile && \

docker build -t ghcr.io/cloudynes/php:$PHPVER-alpine$ALPVER-embed .