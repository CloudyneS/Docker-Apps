ARG PHP_VERSION=8.0
ARG ALPINE_VERSION=3.16
ARG FPM_LISTENER="127.0.0.1:8123"
FROM php:${PHP_VERSION}-fpm-alpine${ALPINE_VERSION}

LABEL Maintainer="Cloudyne Systems"
LABEL Description="PHP-FPM and Nginx Base"
LABEL Version="1.0"

# Set the working directory
RUN mkdir /app
WORKDIR /app

# Set user to root for installation
USER root

# Install additional packages
RUN apk add --no-cache \
    curl msmtp \
    freetype-dev libjpeg-turbo-dev \
    libpng-dev icu-dev icu-data-full \
    libzip-dev imap-dev krb5-dev \
    openssl-dev mysql-client

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

# Overwrite FPM Pool
COPY www.conf /usr/local/etc/php-fpm.d/www.conf
COPY php-fpm.conf /usr/local/etc/php-fpm.conf

RUN rm /usr/local/etc/php-fpm.d/zz-docker.conf

USER nobody

EXPOSE 8123

HEALTHCHECK --interval=5s --timeout=5s --start-period=15s --retries=3 CMD curl -sf http://127.0.0.1:8123/fpm-ping || exit 1