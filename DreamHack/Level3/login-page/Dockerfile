FROM python:3

ENV user login_page
ENV port 8000

RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential
RUN apt-get install mariadb-common mariadb-server mariadb-client -y

RUN pip install --upgrade pip

RUN adduser $user
ADD ./deploy/app /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x run.sh

RUN /bin/bash -c "/usr/bin/mysqld_safe &" && \
  sleep 5 && \
  mysql -uroot < /app/init.sql
RUN rm /app/init.sql

EXPOSE $port

CMD ["./run.sh"]
