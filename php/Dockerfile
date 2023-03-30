ARG PHP_VERSION=8.0
ARG ALPINE_VERSION=3.16
# FROM php:${PHP_VERSION}-cli-alpine${ALPINE_VERSION}

FROM ghcr.io/cloudynes/php:${PHP_VERSION}-alpine${ALPINE_VERSION}-embed

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Extended PHP base image with additional extensions"
LABEL Version="1.0"

USER root
RUN apk add --no-cache \
        curl freetype-dev libjpeg-turbo-dev \
        libpng-dev icu-dev icu-data-full \
        libzip-dev imap-dev krb5-dev \
        openssl-dev mysql-client \
    && rm -rf /var/cache/apk/*

RUN docker-php-ext-configure \
        gd --with-freetype --with-jpeg \
    && docker-php-ext-configure \
        imap --with-kerberos --with-imap-ssl \
    && docker-php-ext-install -j$(nproc) \
        gd \
        intl \
        pdo_mysql \
        mysqli \
        opcache \
        imap \
        zip \
        bcmath \
    && rm -rf /tmp/* /var/cache/apk/* \
    && docker-php-source delete
