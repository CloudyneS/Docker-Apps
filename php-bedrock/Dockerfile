ARG ALPINE_VERSION=3.17
ARG PHP_VERSION=8.1

FROM ghcr.io/cloudynes/php-base:fpm${PHP_VERSION}-alpine${ALPINE_VERSION}

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Lightweight PHP-FPM, Nginx and Bedrock container for Kubernetes based on Alpine Linux."
LABEL Version="1.0"

USER root
RUN mkdir -p /etc/composer && chown nobody.nobody /etc/composer
# COPY --chown=nobody composer-config.json /etc/composer/config.json
COPY composer-config.json /etc/composer/config.json
USER nobody

# FROM cloudyne/php-nginx:${PHP_VERSION}-fpm-alpine${ALPINE_VERSION}
# COPY --from=0 /app /app