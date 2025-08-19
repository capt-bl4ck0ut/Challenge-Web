FROM tiangolo/uwsgi-nginx-flask:python3.10

ENV port 80

ADD ./deploy/app.py /app/app.py
ADD ./deploy/flag.txt /app/flag.txt
ADD ./deploy/static /app/static
ADD ./deploy/templates /app/templates
WORKDIR /app

RUN pip install flask
RUN chmod 444 flag.txt && mv flag.txt /

EXPOSE $port

ENTRYPOINT ["python"]
CMD ["app.py"]
