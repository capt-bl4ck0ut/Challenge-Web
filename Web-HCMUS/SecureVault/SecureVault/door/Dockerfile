FROM python:3.13.5-slim

RUN apt update -y > /dev/null
RUN apt upgrade -y > /dev/null

RUN adduser user

COPY ./app.py /app/app.py

RUN chown -R user:user /app
RUN chmod -R 750 /app
RUN pip3 install pycryptodome

USER user

WORKDIR /app

CMD ["python3", "app.py"]
