FROM python:3.13-slim

ENV USER=user
ENV PORT=3000
ENV FLAG=DH{FAKE_FLAG}

RUN apt-get update && apt-get install -y wget unzip

# install google chrome
RUN wget -O ./google-chrome-stable.deb https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_130.0.6723.116-1_amd64.deb && \
    apt-get install -y ./google-chrome-stable.deb && \
    rm ./google-chrome-stable.deb

# install chromedriver
RUN wget -O ./chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.116/linux64/chromedriver-linux64.zip && \
    unzip chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    rm ./chromedriver.zip

RUN adduser --disabled-password --gecos '' $USER

WORKDIR /app
COPY deploy/ /app/
RUN pip install -r requirements.txt
RUN chown -R $USER:$USER /app

USER $USER
EXPOSE $PORT

CMD ["python", "app.py"]