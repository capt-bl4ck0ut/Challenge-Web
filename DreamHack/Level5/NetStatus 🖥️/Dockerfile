FROM php:7.1.18-apache-stretch
RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
RUN a2enmod rewrite
RUN apt-get update || true
RUN apt-get install --yes vnstat screen netcat
COPY ./htdeploy /var/www/html
RUN mkdir /REDACTED_FLAG_DIR
COPY ./REDACTED_FLAG_DIR /REDACTED_FLAG_DIR
RUN mkdir /deploy
COPY ./deploy /deploy
RUN chmod +x /deploy/log_stats.sh
RUN chmod +x /deploy/run_service.sh
EXPOSE 80
CMD /deploy/run_service.sh