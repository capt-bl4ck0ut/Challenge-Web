FROM node:20-alpine@sha256:2cd2a6f4cb37cf8a007d5f1e9aef090ade6b62974c7a274098c390599e8c72b4

WORKDIR /app

COPY deploy/package.json ./

RUN npm install

COPY deploy/index.js ./
COPY flag.txt ./

EXPOSE 3000

CMD ["node", "index.js"]