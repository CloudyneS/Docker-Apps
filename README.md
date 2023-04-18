# Docker Applications
A collection of docker images for various applications and services.

# Todo
- Install sendmail?



## PHP Images
### alpine/php-embed (Alpha)
Recompiled Alpine PHP images with the --allow-embed option set to be able to compile Nginx Unit.
Tags:
- php-embed:7.4-alpine3.16
- php-embed:8.0-alpine3.16 (stable)
- php-embed:8.1-alpine3.17
- php-embed:8.2-alpine3.17 (latest)

### alpine/php-extended (Alpha)
Based on php-embed with additional extensions for use with unit and Wordpress
Tags:
- php-extended:7.4-alpine3.16
- php-extended:8.0-alpine3.16 (stable)
- php-extended:8.1-alpine3.17
- php-extended:8.2-alpine3.17 (latest)

### alpine/php-unit (Alpha)
Based on php-extended and nginx/unit
Tags:
- php-unit:7.4-unit1.29.0
- php-unit:8.0-unit1.29.1 (stable)
- php-unit:8.1-unit1.29.1
- php-unit:8.2-unit1.29.1 (latest)

### debian/php-unit (Stable)
Based on the official php:*-bullseye images with additional extensions for use with unit and Wordpress
Tags:
- php-slim:7.4-slim-bullseye
- php-slim:8.0-slim-bullseye (stable)
- php-slim:8.1-slim-bullseye
- php-slim:8.2-slim-bullseye (latest)


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
