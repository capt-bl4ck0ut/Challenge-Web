FROM python:3.10-slim-bullseye

ENV USER dreame
ENV PORT 80

# Cài đặt gói cần thiết + MariaDB
RUN apt-get update -y && apt-get install -y \
    python3-pip build-essential wget curl unzip gnupg \
    mariadb-common mariadb-server mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Google Chrome từ repo chính thức
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -y \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Chromedriver (phiên bản latest release)
RUN apt-get update -y && apt-get install -y libnss3 \
    && CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && rm -rf /var/lib/apt/lists/*

# Nâng pip và tạo user
RUN pip install --upgrade pip
RUN adduser --disabled-password $USER

WORKDIR /app

# Copy source code
COPY ./app /app
RUN pip install -r requirements.txt

# Khởi tạo DB
RUN /bin/bash -c "/usr/bin/mysqld_safe &" && \
  sleep 5 && \
  mysql -uroot < /app/init.sql && \
  rm /app/init.sql

# Cho phép run.sh chạy
RUN chmod +x run.sh

EXPOSE $PORT

CMD ["./run.sh"]
