FROM node:21-alpine

ENV USER todo 
ENV PORT 8080
ENV NODE_ENV production
ENV JWT_SECRET_KEY REDACTED_KEY

# Change tmp permissions
RUN chmod 1733 /tmp /var/tmp /dev/shm

# Add user
RUN adduser -D -g "" $USER

# Add files
COPY --chown=$USER:$USER deploy /app


WORKDIR /app
USER $USER
RUN npm install

# Run server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
USER $USER
EXPOSE $PORT
