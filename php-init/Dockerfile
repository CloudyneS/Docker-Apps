ARG ALPINE_VERSION=3.17
ARG PHP_VERSION=8.1
ARG INIT_PACKAGES='nano bash net-tools wget zip tar curl git rsync p7zip python3 py3-pip py3-setuptools'
FROM cloudyne/php-base:${PHP_VERSION}-fpm-alpine${ALPINE_VERSION}

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Lightweight PHP-FPM init container for Kubernetes based on Alpine Linux."
LABEL Version="1.0"

USER root

# Install packages
ARG INIT_PACKAGES
ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache ${INIT_PACKAGES}

# Add composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer; 

# Add WP-CLI
RUN curl -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x /usr/local/bin/wp && \
    wp --info 

# Switch back to nobody
ADD init-py /init-py

RUN cd /init-py && \
    pip3 install -r requirements.txt && \
    mkdir -p /etc/composer && \
    chown -R nobody.nobody /etc/composer /init-py /app && \
    chmod -R 777 /etc/composer

COPY --chown=nobody composer-config.json /etc/composer/config.json
# COPY composer-config.json /etc/composer/config.json

ENV COMPOSER_HOME=/etc/composer
# ENV COMPOSER_ALLOW_SUPERUSER=1

USER nobody

ENTRYPOINT [ "python3" ]
CMD [ "/init-py/init.py" ]
