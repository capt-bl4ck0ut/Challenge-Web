FROM php:8.0-apache

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc curl netcat-traditional

RUN docker-php-ext-install mysqli

COPY ./deploy/src /var/www/html/

COPY ./flag.c /flag.c
RUN gcc /flag.c -o /flag && \
    chmod 111 /flag && \
    rm /flag.c

EXPOSE 80