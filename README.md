# php-apps
PHP containers built for Kubernetes

## Todo
- [ ] Add support and images for PHP8.1
- [ ] Add support and images for PHP7.4
- [ ] Google tag manager plugin
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
