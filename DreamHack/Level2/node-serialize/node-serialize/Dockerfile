FROM node:18-alpine
COPY . /app
WORKDIR /app

RUN apk --no-cache add curl
RUN npm i

CMD ["node","index.js"]