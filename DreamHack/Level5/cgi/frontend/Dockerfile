FROM python:3.10.14-bullseye

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

COPY ./src /src
COPY ./requirements.txt /src/

WORKDIR /src

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "app.py"]
