FROM mysql:8.0-debian

ENV MYSQL_RANDOM_ROOT_PASSWORD=yes
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password
ENV MYSQL_DATABASE=colorfulmemo
ENV TZ=Asia/Seoul
ENV OPENSSL_CONF=/dev/null

RUN sed -i 's/deb.debian.org/mirror.kakao.com/g' /etc/apt/sources.list 

RUN apt-get update -y \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends -y \
        gcc wget bzip2 python3-pip python3-setuptools \
        software-properties-common apache2 php php-mysqli \
        chrpath libssl-dev libxft-dev \
        libfreetype6 libfreetype6-dev \
        libfontconfig1 libfontconfig1-dev \
 && rm -rf /var/lib/apt/lists/* /var/www/html/*

COPY ./src/ /var/www/html/
RUN chmod -R 755 /var/www/html

RUN wget -q -O /root/phantomjs-2.1.1-linux-x86_64.tar.bz2 \
    https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 \
 && tar -C /root/ -jxf /root/phantomjs-2.1.1-linux-x86_64.tar.bz2 \
 && cp /root/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /bin/ \
 && rm -rf /root/phantomjs*

RUN pip3 install --no-cache-dir selenium==2.48.0

COPY ./bot.py /bot.py
RUN chmod 755 /bot.py

# Config files
COPY mysql/config/ /etc/mysql/

RUN chown -R www-data:www-data /var/lib/mysql /var/run/mysqld

COPY ./init.sql /docker-entrypoint-initdb.d

EXPOSE 80
EXPOSE 3306

COPY ./run.sh /run.sh
RUN chmod 755 /run.sh

COPY --chown=root:www-data ./flag /flag
RUN chmod 440 /flag && \
    mv /flag /flag_$(md5sum /flag | awk '{print $1}')

ENTRYPOINT ["/run.sh"]