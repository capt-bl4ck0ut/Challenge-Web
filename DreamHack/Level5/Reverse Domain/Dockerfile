FROM node:current-alpine

WORKDIR /app
COPY ./app /app

RUN npm install
RUN npm install pm2 -g

RUN mkdir /usr/share/fonts
RUN mkdir /usr/share/fonts/nanumfont
RUN wget http://cdn.naver.com/naver/NanumFont/fontfiles/NanumFont_TTF_ALL.zip
RUN unzip NanumFont_TTF_ALL.zip -d /usr/share/fonts/nanumfont
RUN apk add fontconfig
RUN fc-cache -f -v

ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR.UTF-8

EXPOSE 80
ENTRYPOINT ["pm2-runtime", "start", "app.js"]