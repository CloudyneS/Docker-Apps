ARG PHP_VERSION=8.0
ARG ALPINE_VERSION=3.16
FROM ghcr.io/cloudynes/php:${PHP_VERSION}-alpine${ALPINE_VERSION}-embed

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Extended PHP base image with additional extensions"
LABEL Version="1.0"

# Compile-time dependencies
ENV PHPIZE_DEPS \
        dpkg-dev dpkg \
		file \
		g++ \
		gcc \
		libc-dev \
		make \
		pkgconf \
		re2c \
        autoconf \
        freetype-dev \
        libjpeg-turbo-dev \
        libpng-dev \
        libwebp-dev \
        icu-dev \
        icu-data-full \
        libzip-dev \
        imap-dev \
        krb5-dev \
        openssl-dev \
        mysql-client

# Runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    curl \
    tar \
    xz \
    mysql-client \
    openssl

RUN set -eux; \
    apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
        ; \
    docker-php-ext-configure \
        gd --with-freetype --with-jpeg ; \
    docker-php-ext-configure \
        imap --with-kerberos --with-imap-ssl ; \
    docker-php-ext-install -j$(nproc) \
        gd \
        intl \
        pdo_mysql \
        mysqli \
        opcache \
        imap \
        zip \
        bcmath \
        ; \
    docker-php-source delete; \
    runDeps="$( \
		scanelf --needed --nobanner --format '%n#p' --recursive /usr/local \
			| tr ',' '\n' \
			| sort -u \
			| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
	)"; \
	apk add --no-cache $runDeps; \
	apk del --no-network .build-deps; \
    rm -rf /tmp/* /var/cache/apk/*

