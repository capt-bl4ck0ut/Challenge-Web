FROM node:20-alpine

WORKDIR /app

RUN apk --no-cache add curl
RUN apk add --no-cache python3 py3-pip

COPY ./ /app/
RUN pip3 install -r /app/requirements.txt --break-system-packages

RUN npm install -g dreamhack-cli@1.1.0
RUN sed -i '38s/.*/try {/' /usr/local/lib/node_modules/dreamhack-cli/src/command/create.js
RUN sed -i '47s/.*/} catch (err) {}/' /usr/local/lib/node_modules/dreamhack-cli/src/command/create.js
RUN sed -i '8s~.*~&\nif(/[!@#$%^*(){}|<>]/.test(outputLocationPath)) return false;~' /usr/local/lib/node_modules/dreamhack-cli/src/util/downloadFile.js

EXPOSE 5000
CMD ["python3", "app.py"]