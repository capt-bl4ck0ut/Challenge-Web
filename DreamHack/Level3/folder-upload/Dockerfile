FROM python:3.10-slim
WORKDIR /app
COPY app.py .
COPY flag.txt .
COPY templates ./templates
RUN pip install flask lxml requests
EXPOSE 8000
CMD ["python", "app.py"]