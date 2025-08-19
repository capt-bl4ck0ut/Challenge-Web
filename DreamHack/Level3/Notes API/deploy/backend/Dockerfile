FROM python:3.11-alpine@sha256:c6bb0934b659c1098ff8d10e5c8c0dd3b7bbfd856523af70eb73f8641c54b738

ENV USER backend

# Add user
RUN adduser -D -g "" $USER

# Add files
RUN mkdir app
COPY --chown=root:root main.py /app/main.py
COPY --chown=root:root requirements.txt /app/requirements.txt
COPY --chown=root:root run.sh /app/run.sh
COPY --chown=root:$USER flag /flag

WORKDIR /app
RUN chmod 705 run.sh
RUN pip install -r requirements.txt

USER $USER
ENTRYPOINT ["/bin/ash"]
CMD ["./run.sh"]
