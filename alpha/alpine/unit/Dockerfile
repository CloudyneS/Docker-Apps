ARG PHP_VERSION=8.0
ARG ALPINE_VERSION=3.16
ARG UNIT_VERSION=1.29.1
FROM ghcr.io/cloudynes/php:${PHP_VERSION}-alpine${ALPINE_VERSION} AS BUILDER

LABEL Maintainer="Cloudyne Systems"
LABEL Description="PHP base image with NGINX Unit"
LABEL Version="1.0"


ARG UNIT_VERSION
RUN set -ex \
    && apk add --no-cache \
        ca-certificates mercurial \
        alpine-sdk pcre2-dev gcc \
    && rm -rf /var/cache/apk/*

RUN set -ex \
    mkdir -p /usr/lib/unit/modules /usr/lib/unit/debug-modules \
    && hg clone https://hg.nginx.org/unit \
    && cd unit \
    && hg up ${UNIT_VERSION} \
    && NCPU="$(getconf _NPROCESSORS_ONLN)" \
    && CONFIGURE_ARGS="\
        --prefix=/usr \
        --state=/var/lib/unit \
        --control=unix:/run/control.unit.sock \
        --pid=/run/unit.pid \
        --log=/var/log/unit.log \
        --modules=/usr/lib/unit/modules \
        --openssl \
        --user=unit \
        --group=unit \
        --tests" \
    && ./configure \
        $CONFIGURE_ARGS \
        --modules=/usr/lib/unit/debug-modules \
        --debug \
    && make -j $NCPU unitd \
    && install -pm755 build/unitd /usr/sbin/unitd-debug \
    && make clean \
    && ./configure \
        $CONFIGURE_ARGS \
        --modules=/usr/lib/unit/debug-modules \
    && make -j $NCPU unitd \
    && install -pm755 build/unitd /usr/sbin/unitd \
    && make clean \
    \
    && ./configure \
        $CONFIGURE_ARGS \
        --modules=/usr/lib/unit/debug-modules \
        --debug \
    && ./configure php \
    && make -j $NCPU php-install \
    && make clean \
    && ./configure \
        $CONFIGURE_ARGS \
        --modules=/usr/lib/unit/modules \
    && ./configure php \
    && make -j $NCPU php-install

FROM ghcr.io/cloudynes/php:${PHP_VERSION}-alpine${ALPINE_VERSION}

# COPY docker-entrypoint.sh /usr/local/bin/
COPY --from=BUILDER /usr/sbin/unitd /usr/sbin/unitd
COPY --from=BUILDER /usr/sbin/unitd-debug /usr/sbin/unitd-debug
COPY --from=BUILDER /usr/lib/unit/ /usr/lib/unit/


STOPSIGNAL SIGTERM