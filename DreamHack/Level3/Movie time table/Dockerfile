FROM eclipse-temurin:17-jdk-jammy

ENV USER=james
ENV PORT=8080

RUN adduser --disabled-password $USER -u 1337

WORKDIR /app

COPY ./deploy/flag /
COPY ./deploy/table.xml ./tables/
COPY ./deploy/Cinema-0.0.1-SNAPSHOT.jar .

USER $USER
EXPOSE $PORT

CMD ["java","-jar","./Cinema-0.0.1-SNAPSHOT.jar"]