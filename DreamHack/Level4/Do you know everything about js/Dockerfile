FROM node:22-alpine AS frontend-build
WORKDIR /src/frontend
ENV YARN_NODE_LINKER=node-modules
RUN corepack enable
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile
COPY frontend/ .
RUN yarn build

FROM node:22-alpine AS backend-build
WORKDIR /src/backend
ENV YARN_NODE_LINKER=node-modules
RUN corepack enable
COPY backend/package.json backend/yarn.lock ./
RUN yarn install --frozen-lockfile
COPY backend/ .
RUN yarn build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV NITRO_HOST=0.0.0.0
ENV NITRO_PORT=8080
ENV PORT=3000
ENV BACKEND_HOST=127.0.0.1
ENV BACKEND_PORT=3000
ENV NUXT_PUBLIC_API_BASE="/api"
ENV YARN_NODE_LINKER=node-modules
COPY --from=frontend-build /src/frontend/.output ./frontend/.output
COPY --from=backend-build /src/backend/dist ./backend/dist
COPY --from=backend-build /src/backend/package.json ./backend/package.json
COPY --from=backend-build /src/backend/yarn.lock ./backend/yarn.lock
WORKDIR /app/frontend/.output/server
RUN corepack enable && yarn install --production
WORKDIR /app/backend
RUN corepack enable && yarn install --frozen-lockfile --production
WORKDIR /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8080
CMD ["/entrypoint.sh"]
