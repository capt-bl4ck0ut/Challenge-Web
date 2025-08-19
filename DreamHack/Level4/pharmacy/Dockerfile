FROM php:7.4-apache

COPY ./deploy/run.sh /usr/sbin/
RUN chmod +x /usr/sbin/run.sh

COPY ./deploy/src /var/www/html
RUN chmod 777 /var/www/html/uploads

COPY ./deploy/flag.txt /

EXPOSE 80
CMD ["/usr/sbin/run.sh"]