#!/bin/bash
git clone https://github.com/docker-library/php.git ./php-alpine-embed/php-alpine-original && \
        
sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' ./php-alpine-embed/php-alpine-original/8.0/alpine3.16/cli/Dockerfile && \
sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' ./php-alpine-embed/php-alpine-original/8.1/alpine3.17/cli/Dockerfile && \
sed -i 's/--enable-option-checking=fatal \\/--enable-option-checking=fatal --enable-embed \\/' ./php-alpine-embed/php-alpine-original/8.2/alpine3.17/cli/Dockerfile && \