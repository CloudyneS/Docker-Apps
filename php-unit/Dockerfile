ARG PHP_VERSION=8.1
# FROM php:${PHP_VERSION}-cli-alpine
FROM nginx/unit:1.29.1-php${PHP_VERSION}

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Nginx Unit and PHP image"
LABEL Version="1.0"

# Set the working directory
RUN mkdir /app
WORKDIR /app

# Set user to root for installation
USER root

# Install additional packages
# RUN apk add --no-cache \
RUN apt-get update 

RUN apt-get -y install \
    zlib1g-dev libfreetype6-dev \
    curl libjpeg-dev \
    libicu-dev libpng-dev \
    libssl-dev mariadb-client

RUN apt-get -y install \
    libzip-dev default-libmysqlclient-dev \
    libc-client-dev libkrb5-dev

# Preconfigure PHP Packages
RUN docker-php-ext-configure gd --with-freetype --with-jpeg && \
    docker-php-ext-configure imap --with-kerberos --with-imap-ssl

# Install additional PHP packages
RUN docker-php-ext-install -j$(nproc) \
    gd \
    intl \
    pdo_mysql \
    mysqli \
    opcache \
    imap \
    zip \
    bcmath

# RUN mkdir /var/lib/unit/certs
# RUN chown -R nobody.nobody /var/lib/unit/certs /run

COPY config.json /docker-entrypoint.d/config.json

# USER nobody
# ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
# CMD 
# CMD [ "unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock" ]

EXPOSE 8080