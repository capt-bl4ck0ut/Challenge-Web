FROM python:3.13.3-alpine
WORKDIR /app
RUN adduser -D dat2phit

COPY . .
RUN pip install -r requirements.txt

USER dat2phit
# EXPOSE 9812

CMD [ "python3", "main.py", "-z", "7" ]