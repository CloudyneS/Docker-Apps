#!/bin/bash
rm -rf ./php-alpine-original; \
git clone https://github.com/docker-library/php.git ./php-alpine-original; \

sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' 8.0/Dockerfile && \
sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' 8.1/Dockerfile && \
sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' 8.2/Dockerfile

