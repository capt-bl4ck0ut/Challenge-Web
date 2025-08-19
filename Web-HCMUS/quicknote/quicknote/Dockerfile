FROM php:8.2-apache

RUN a2enmod rewrite

RUN mkdir -p /quicknote

COPY src/ /var/www/html/

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chown -R www-data:www-data /quicknote \
    && chmod -R 755 /quicknote

EXPOSE 80