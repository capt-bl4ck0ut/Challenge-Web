FROM node:21.5-slim@sha256:c88704924204ee6d4e9da02275a8fd27355502f7177e4175cd0d3a4375a9c9c8

ENV NODE_ENV production
ENV PORT 7000
ENV USER app

# Add user
RUN adduser --disabled-password --gecos "" --uid 1001 $USER

# Set working directory
RUN mkdir /app
WORKDIR /app

# Add files
COPY --chown=root:root server.js /app/
COPY --chown=root:root templates /app/templates
COPY --chown=root:root package.json /app/
COPY --chown=root:root package-lock.json /app/

# Install dependencies
RUN npm install

USER $USER
EXPOSE $PORT
CMD while :; do sleep 0.5; node server.js; done
