ARG SOURCE_VERSION
FROM ghcr.io/cloudynes/php-unit:${SOURCE_VERSION} AS BUILDER

LABEL Version="1.0"
LABEL Maintainer="Cloudyne Systems"
LABEL org.opencontainers.image.source="https://github.com/cloudynes/docker-apps"
LABEL Description="Container for Roots Bedrock based on extended PHP image with Nginx Unit"
LABEL org.opencontainers.image.description="Container for Roots Bedrock based on extended PHP image with Nginx Unit"
LABEL org.opencontainers.image.licenses="MIT"

# Set the working directory and installation user
USER root

WORKDIR /app

# Install GIT and Composer
RUN apt-get update && apt-get -y install git && apt-get clean \ 
    && chown -R unit:unit /app \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer create-project --no-interaction --no-dev roots/bedrock .

FROM ghcr.io/cloudynes/php-unit:${SOURCE_VERSION}

USER root
WORKDIR /app

COPY --from=BUILDER --chown=unit:unit /app /app
COPY --chown=unit:unit ./config.json /docker-entrypoint.d/unit.json

ENV WP_CLI_CACHE_DIR="/tmp/wpcli/cache"             \
    WP_CLI_CONFIG_PATH="/etc/wpcli/wpcli.conf"      \
    WP_CLI_PACKAGES_DIR="/etc/wpcli/packages"

# Add WP-CLI and clear folders/caches
RUN curl -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
    && chmod +x /usr/local/bin/wp && mkdir -p /etc/wpcli/packages && chown -R unit:unit /etc/wpcli

USER unit

RUN /usr/local/bin/wp package install aaemnnosttv/wp-cli-dotenv-command

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD [ "unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock" ]

EXPOSE 8080