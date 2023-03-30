# Docker Applications
A collection of docker images for various applications and services.

## PHP Images
### php:\*.\*-alpine\*.\*\*-embed
PHP Images built with the --allow-embed option for use with Nginx Unit

### php:\*.\*-alpine\*.\*\*
The embed image from above with additional extensions installed for use with unit and Wordpress

### ghcr.io/cloudynes/php-unit:\*.\*-\*.\*.\*\*-unit\*.\*\*.\*
Alpine image with Nginx Unit based on the cloudyne/php-images

### php
PHP Images with the following extensions added:
# php-apps
PHP containers built for Kubernetes

### Unit Todo
- Build with follow_symlinks option
- Index not working



## Sendmail Configuration
Environment variables:

## PHP 8.0
### PHP Base
Source: php:8.0-fpm-alpine3.16
User: nobody (65534)
Additional PHP extensions:
- gd
- intl
- pdo_mysql
- mysqli
- opcache
- imap
- zip
- bcmath
FPMPool Configuration:
- Listener: 127.0.0.1:8123
- Listen Backlog: 511
- PM: ondemand
- PM Max Children: 100
- PM Process Idle Timeout: 30s
- PM Max Requests: 1000
- Ping Path: /fpm-ping
- Security Limit Extensions: .php
- Date.timezone: Europe/Stockholm
- Expose PHP: Off
- Disable Functions: exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,show_source
- Upload Max Filesize: 256M
- Post Max Size: 256M

### PHP Nginx
