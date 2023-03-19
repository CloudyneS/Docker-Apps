ARG ALPINE_VERSION=3.16
ARG PHP_VERSION=8.0
ARG INIT_PACKAGES='sudo nano bash net-tools wget zip tar curl git rsync p7zip python3 py3-pip py3-setuptools'
FROM ghcr.io/cloudynes/php-base:fpm${PHP_VERSION}-alpine${ALPINE_VERSION}

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Lightweight PHP-FPM init container for Kubernetes based on Alpine Linux."
LABEL Version="1.0"

# Initializations will be done using the root user
# for the ability to chown folders, files and shares
USER root

# Set environment variables
ENV PYTHONUNBUFFERED=1                              \
    COMPOSER_HOME="/etc/composer"                   \
    WP_CLI_CACHE_DIR="/tmp/wpcli-cache"             \
    WP_CLI_CONFIG_PATH="/etc/wpcli/wpcli.conf"      \
    WP_CLI_PACKAGES_DIR="/etc/wpcli/packages"

# Install additional packages for init
ARG INIT_PACKAGES
RUN apk add --no-cache ${INIT_PACKAGES}

# Add the initialization scripts
ADD init-py /init-py

RUN mkdir -p /etc/composer /etc/wpcli/packages && \
    curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer && \
    pip3 install -r /init-py/requirements.txt && \
    chown -R nobody.root /etc/composer /etc/wpcli /init-py && \
    chmod -R 770 /etc/composer /etc/wpcli /init-py && \
    sudo -u nobody -E /usr/local/bin/wp package install aaemnnosttv/wp-cli-dotenv-command

# Add custom repository configuration
COPY --chown=nobody composer-config.json /etc/composer/config.json

ENTRYPOINT [ "" ]

CMD [ "/bin/bash", "/init-py/init.sh" ]
