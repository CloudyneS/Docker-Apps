#!/bin/bash
rm -rf /tmp/php-docker && \
git clone https://github.com/docker-library/php.git /tmp/php-docker && \


cp -r /tmp/php-docker/8.0/alpine3.16/cli/* ./8.0/ && \
cp -r /tmp/php-docker/8.1/alpine3.17/cli/* ./8.1/ && \
cp -r /tmp/php-docker/8.2/alpine3.17/cli/* ./8.2/ && \

sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' 8.0/Dockerfile && \
sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' 8.1/Dockerfile && \
sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' 8.2/Dockerfile
