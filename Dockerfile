FROM python:3.8-alpine3.10

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

RUN apk update
RUN apk add chromium chromium-chromedriver

RUN pip install selenium

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pytest login-tests.py