ARG SOURCE_VERSION
FROM ghcr.io/cloudynes/php-unit:${SOURCE_VERSION}

LABEL Version="1.0"
LABEL Maintainer="Cloudyne Systems"
LABEL org.opencontainers.image.source="https://github.com/cloudynes/docker-apps"
LABEL Description="Container for Roots Bedrock based on extended PHP image with Nginx Unit"
LABEL org.opencontainers.image.description="Container for Roots Bedrock based on extended PHP image with Nginx Unit"
LABEL org.opencontainers.image.licenses="MIT"

# Set the working directory and installation user
USER root
WORKDIR /app

# ENV COMPOSER_HOME="/etc/composer"                   \
ENV WP_CLI_CACHE_DIR="/tmp/wpcli-cache"             \
    WP_CLI_CONFIG_PATH="/etc/wpcli/wpcli.conf"      \
    WP_CLI_PACKAGES_DIR="/etc/wpcli/packages"

# Uncomment these two lines to add Composer and composer-config.json
# RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer && \
#     mkdir -p /etc/composer && chown -R unit:unit /etc/composer && apt-get update && apt-get -y install git && apt-get clean 
# ADD ./composer-config.json /etc/composer/config.json

# # Add WP-CLI
RUN curl -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar; chmod +x /usr/local/bin/wp; \
    wp --info --allow-root

COPY config.json /docker-entrypoint.d/config.json

RUN mkdir -p /app && chown -R unit:unit /app && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

USER unit

# Uncomment this line to preinstall Bedrock
# RUN composer create-project --no-dev --no-interaction roots/bedrock .

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD [ "unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock" ]

EXPOSE 8080