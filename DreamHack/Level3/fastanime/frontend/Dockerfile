FROM node:20.10.0-alpine

WORKDIR /frontend

COPY package.json .

RUN npm install

COPY . .

CMD ["node", "app"]