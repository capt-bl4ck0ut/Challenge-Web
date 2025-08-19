FROM python:3.13.3-alpine
WORKDIR /app

RUN adduser -D dat2phit

COPY flag /flag
RUN mv /flag /flag_$(tr -dc A-Za-z0-9 </dev/urandom | head -c 10)

COPY . .
RUN pip install -r requirements.txt

EXPOSE 1337

USER dat2phit

CMD [ "python3", "app.py"]