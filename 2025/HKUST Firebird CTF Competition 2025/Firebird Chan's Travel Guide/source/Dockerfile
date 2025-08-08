FROM python:3.11.3-alpine3.18

RUN apk --no-cache add chromium chromium-chromedriver

RUN pip install flask && pip install selenium && pip install flask_limiter && pip install pyjwt

ENV FLAG=firebird{REDACTED}

COPY /env /

CMD ["python","/app.py"]