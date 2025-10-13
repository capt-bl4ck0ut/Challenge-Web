FROM ubuntu:22.04

RUN apt-get update

RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y nodejs
RUN apt-get install -y npm

COPY ./ /prob/

WORKDIR /prob/SeonFlower~_~


EXPOSE 9000
EXPOSE 9001

RUN npm install
RUN pip3 install -r ./requirements.txt

RUN chmod 777 ./start.sh

CMD ["./start.sh"]
