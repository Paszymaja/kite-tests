FROM python:3.8-alpine3.10

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

RUN apk update
RUN apk add chromium chromium-chromedriver

WORKDIR /app

COPY requirements.txt .
RUN pip install --quiet -r requirements.txt

COPY data ./data
COPY scripts ./scripts

COPY login-tests.py .
CMD ["pytest", "./login-tests.py"]