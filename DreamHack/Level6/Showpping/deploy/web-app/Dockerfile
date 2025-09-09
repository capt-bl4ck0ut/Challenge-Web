FROM node:20

ENV USER developer
ENV PORT 3000

RUN adduser --disabled-password $USER

# RUN apk update && apk add curl chromium gcc musl-dev

RUN apt-get update \
    && apt-get install -y gcc wget gnupg sqlite3 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 --no-install-recommends\
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# FLAG
COPY ./flag.c /flag.c
RUN gcc /flag.c -o /flag && \
    chmod 111 /flag && rm /flag.c && rm /app/flag.c && \
    chown $USER:$USER /flag

RUN chmod +x ./entrypoint.sh

EXPOSE $PORT

ENTRYPOINT ["./entrypoint.sh"]
CMD ["node", "app.js"]