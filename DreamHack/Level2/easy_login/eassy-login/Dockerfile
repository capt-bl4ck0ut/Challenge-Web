FROM php:7.3-apache

COPY ./deploy/run.sh /usr/sbin/
RUN chmod +x /usr/sbin/run.sh

COPY ./deploy/src /var/www/html

EXPOSE 80
CMD ["/usr/sbin/run.sh"]
