FROM python:3.13.5-slim

RUN apt update -y > /dev/null
RUN apt upgrade -y > /dev/null

RUN adduser user

COPY ./flag.txt /app/flag.txt

RUN chown -R user:user /app
RUN chmod -R 750 /app

USER user

WORKDIR /app

CMD ["python3", "-m", "http.server", "6969"]
