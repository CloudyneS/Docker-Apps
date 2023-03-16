ARG ALPINE_VERSION=3.17
ARG PHP_VERSION=8.1
FROM ghcr.io/cloudynes/php-base:fpm${PHP_VERSION}-alpine${ALPINE_VERSION}

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Lightweight PHP-FPM and Nginx container for Kubernetes based on Alpine Linux."
LABEL Version="1.0"

USER root

RUN apk add --no-cache nginx supervisor
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisor.conf /etc/supervisor/conf.d/supervisord.conf

RUN chown -R nobody.nobody \
    /run \
    /app \
    /var/lib/nginx \
    /var/log/nginx

USER nobody

EXPOSE 8080

ENTRYPOINT [""]

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

HEALTHCHECK --interval=5s --timeout=5s --start-period=15s --retries=3 CMD curl -sf http://127.0.0.1:8080/fpm-ping || exit 1