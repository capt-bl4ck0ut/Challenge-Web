FROM openjdk:18

ARG WAR_FILE=chall-0.0.1-SNAPSHOT.war
RUN mkdir -p /usr/local/app
WORKDIR /usr/local/app

RUN adduser --system dreampring
RUN chown dreampring:dreampring .
USER dreampring:dreampring

COPY ./deploy/${WAR_FILE} /usr/local/app/app.war
RUN jar -xvf app.war
WORKDIR /usr/local/app/WEB-INF/
RUN mkdir ./data/
COPY ./deploy/flag.properties ./classes/flag.properties

ENTRYPOINT ["java", "-classpath", "lib/*:classes/.", "com.dreamhack.chall.MainApplication"]
