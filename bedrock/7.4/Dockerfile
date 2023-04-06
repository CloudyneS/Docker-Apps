FROM ghcr.io/cloudynes/php-unit:7.4

LABEL Maintainer="Cloudyne Systems"
LABEL Description="Nginx Unit and PHP image"
LABEL Version="1.0"

# Set the working directory
WORKDIR /app

ENV COMPOSER_HOME="/etc/composer"                   \
    WP_CLI_CACHE_DIR="/tmp/wpcli-cache"             \
    WP_CLI_CONFIG_PATH="/etc/wpcli/wpcli.conf"      \
    WP_CLI_PACKAGES_DIR="/etc/wpcli/packages"

# Add WP-CLI
RUN curl -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar; chmod +x /usr/local/bin/wp; wp --info

# Add Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

COPY config.json /docker-entrypoint.d/config.json

RUN mkdir -p /app /etc/composer && chown -R unit:unit /app /etc/composer && apt-get update && apt-get -y install git; \
    mkdir -p /var/lib/unit && chown -R unit:unit /var/run /run /var/lib/unit

USER unit

RUN composer create-project --no-dev --no-interaction roots/bedrock .

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD [ "unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock" ]

EXPOSE 8080