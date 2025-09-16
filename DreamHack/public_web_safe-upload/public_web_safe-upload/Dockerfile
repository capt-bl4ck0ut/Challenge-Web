FROM php:8.2-apache

RUN apt-get update && apt-get install -y --no-install-recommends \
    yara ca-certificates file \
 && rm -rf /var/lib/apt/lists/*

ARG PHP_UPLOAD_MAX=10M
ENV PHP_UPLOAD_MAX=${PHP_UPLOAD_MAX}
RUN { \
      echo "file_uploads = On"; \
      echo "upload_max_filesize = ${PHP_UPLOAD_MAX}"; \
      echo "post_max_size = ${PHP_UPLOAD_MAX}"; \
      echo "max_file_uploads = 10"; \
      echo "expose_php = Off"; \
    } > /usr/local/etc/php/conf.d/uploads.ini

RUN mkdir -p /var/www/html/tmp /var/www/html/uploads /var/app/rules \
 && chown -R www-data:www-data /var/www/html/tmp /var/www/html/uploads

COPY public/ /var/www/html/
COPY rules/  /var/app/rules/

RUN echo 'cybercon{REDACTED}' > /$(mktemp -u XXXXXXXXXXXX).txt