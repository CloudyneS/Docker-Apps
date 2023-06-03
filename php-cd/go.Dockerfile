ARG SOURCE_VERSION=8.2
FROM golang:1.18-buster as BUILDER

LABEL Version="1.0"
LABEL Maintainer="Cloudyne Systems"
LABEL org.opencontainers.image.source="https://github.com/cloudynes/docker-apps"
LABEL Description="Container for initializing PHP installations in an effort to keep base image size smaller"
LABEL org.opencontainers.image.description="Container for initializing PHP installations in an effort to keep base image size smaller"
LABEL org.opencontainers.image.licenses="MIT"

USER root
WORKDIR /init-go
ADD init-go /init-go

RUN go build -o init-go main.go

FROM cloudyne.azurecr.io/php-bedrock:${SOURCE_VERSION}

ENV CD_CONFIG="/init-go/config.json"

USER root
WORKDIR /init-go

COPY --from=BUILDER /init-go/init-go /init-go/init-go

COPY ./init-go/config-sample.json /init-go/config.json

WORKDIR /app
ENTRYPOINT [ "" ]
CMD [ "/init-go/init-go" ]
