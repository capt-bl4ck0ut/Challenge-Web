# pypy:3.9-7.3.11-slim
FROM pypy@sha256:50db3f9fc59d050725061579424edd6555bbe932a32834928657ef276e9e2f9a

RUN useradd -m server
USER server
WORKDIR /home/server

COPY deploy/chall/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY --chown=server:server deploy/chall /home/server/chall
COPY --chown=server:server deploy/run-chall.sh /home/server/run-chall.sh
COPY --chown=server:server deploy/secrets/flag.txt /tmp/flag.txt
COPY --chown=server:server deploy/secrets/admin_password.txt /tmp/admin_password.txt

EXPOSE 55000
CMD ["bash", "/home/server/run-chall.sh"]
