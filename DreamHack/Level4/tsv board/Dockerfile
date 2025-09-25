FROM node:20-alpine@sha256:1a526b97cace6b4006256570efa1a29cd1fe4b96a5301f8d48e87c5139438a45
ENV NODE_ENV=production

COPY . /app
WORKDIR /app

RUN npm install
CMD ["npm", "start"]

EXPOSE 8000
