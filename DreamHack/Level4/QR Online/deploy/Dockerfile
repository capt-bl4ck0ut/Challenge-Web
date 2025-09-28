FROM python:3.10-alpine

ENV USER qr
ENV PORT 8000

RUN adduser --disabled-password $USER

RUN mkdir /app
ADD ./app/requirements.txt /app

WORKDIR /app
RUN pip install -r requirements.txt

ADD ./app /app

RUN mkdir -p static/users
RUN chmod 777 static/users
RUN mkdir -p static/cache
RUN chmod 777 static/cache

RUN chmod +x run.sh

USER $USER
EXPOSE $PORT

CMD ["./run.sh"]
