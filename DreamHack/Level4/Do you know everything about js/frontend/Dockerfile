FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN corepack enable && yarn install --frozen-lockfile
COPY . .
RUN yarn build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app ./
ENV HOST 0.0.0.0
EXPOSE 8080
CMD ["yarn", "preview", "--port", "8080"]
