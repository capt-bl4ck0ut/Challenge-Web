FROM php:7.3-apache

COPY ./public /var/www/html
RUN chmod -R 755 /var/www/html
RUN chmod -R 1777 /var/www/html/uploads
RUN chown root:root /var/www/html
ENV SECRET_KEY "<redacted>"

# flag 1
ENV FLAG1 "<redacted>"
# flag 2
RUN echo "<redacted>" > "/flag2-$(head -c 8 /dev/urandom | od -A n -t x1 | tr -d ' \n')"
RUN chmod -R 755 /flag*

EXPOSE 80