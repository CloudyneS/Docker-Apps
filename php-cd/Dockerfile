ARG SOURCE_VERSION=8.2
ARG INIT_PACKAGES='sudo nano bash net-tools wget zip tar curl git rsync p7zip python3 python3-pip python3-setuptools mariadb-client'
FROM ghcr.io/cloudynes/php-unit:${SOURCE_VERSION}

LABEL Version="1.0"
LABEL Maintainer="Cloudyne Systems"
LABEL org.opencontainers.image.source="https://github.com/cloudynes/docker-apps"
LABEL Description="Container for initializing PHP installations in an effort to keep base image size smaller"
LABEL org.opencontainers.image.description="Container for initializing PHP installations in an effort to keep base image size smaller"
LABEL org.opencontainers.image.licenses="MIT"

# Set environment variables
ENV PYTHONUNBUFFERED=1                              \
    COMPOSER_HOME="/etc/composer"                   \
    WP_CLI_CACHE_DIR="/tmp/wpcli-cache"             \
    WP_CLI_CONFIG_PATH="/etc/wpcli/wpcli.conf"      \
    WP_CLI_PACKAGES_DIR="/etc/wpcli/packages"

# Initializations will be done using the root user
# for the ability to chown folders, files and shares
USER root

# Install additional packages for init
ARG INIT_PACKAGES
RUN apt-get update && apt-get -y install ${INIT_PACKAGES} && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add WP-CLI
RUN curl -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar; chmod +x /usr/local/bin/wp; wp --info

# Add Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Add the initialization scripts
ADD init-py /init-py

RUN mkdir -p /etc/composer /etc/wpcli/packages && \
    pip3 install -r /init-py/requirements.txt && \
    chown -R unit.root /etc/composer /etc/wpcli /init-py && \
    chmod -R 770 /etc/composer /etc/wpcli /init-py && \
    sudo -u unit -E /usr/local/bin/wp package install aaemnnosttv/wp-cli-dotenv-command

# Add custom repository configuration
COPY --chown=unit composer-config.json /etc/composer/config.json

RUN mkdir -p /app /etc/composer && chown -R unit:unit /app /etc/composer && apt-get update && apt-get -y install git; apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

ENTRYPOINT [ "" ]

CMD [ "/bin/bash", "/init-py/init.sh" ]
