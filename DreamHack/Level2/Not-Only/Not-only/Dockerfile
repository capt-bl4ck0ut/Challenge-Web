FROM node:16-bullseye

ENV APP_USER=mongodb
ENV APP_PORT=3000

RUN groupadd -g 1234 $APP_USER && useradd -r -u 1234 -g $APP_USER $APP_USER

RUN apt-get update && apt-get install -y gnupg wget ca-certificates \
    && wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add - \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list \
    && apt-get update \
    && apt-get install -y mongodb-org bash \
    && rm -rf /var/lib/apt/lists/*

ADD ./deploy /app
WORKDIR /app

RUN mkdir -p /data/db && chown $APP_USER:$APP_USER /data/db
RUN npm install --global npm \
    && mv docker-entrypoint.sh /usr/local/bin/ \
    && chmod 777 /usr/local/bin/docker-entrypoint.sh

USER $APP_USER
EXPOSE $APP_PORT

ENTRYPOINT ["docker-entrypoint.sh"]
