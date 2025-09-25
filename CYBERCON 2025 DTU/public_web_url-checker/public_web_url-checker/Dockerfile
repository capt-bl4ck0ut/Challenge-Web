FROM php:8.2-apache

RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-server wget unzip less ca-certificates libzip-dev \
    libjpeg62-turbo-dev libfreetype6-dev libpng-dev \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install pdo_mysql mysqli gd \
 && a2enmod rewrite \
 && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
 && chmod +x /usr/local/bin/wp
COPY index.php /var/www/html/index.php
COPY space.css /var/www/html/space.css
COPY plugins/web-directory-free.zip /tmp/web-directory-free.zip
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY apache-cms-local.conf /etc/apache2/conf-available/cms-local.conf
RUN a2enconf cms-local

ENV WP_VERSION=6.8.2 \
    WP_URL=http://localhost:8080/cms \
    WP_TITLE="Only local WordPress" \
    WP_ADMIN_USER=admin \
    WP_ADMIN_PASS=<REDACTED> \
    WP_ADMIN_EMAIL=admin@example.com \
    DB_NAME=wordpress \
    DB_USER=wp \
    DB_PASS=<REDACTED>

EXPOSE 80
CMD ["/entrypoint.sh"]
