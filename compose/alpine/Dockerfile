FROM alpine:latest

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    build-base \
    libffi-dev \
    && pip3 install --upgrade pip \
    && pip3 install numpy pandas \
    && pip3 install --no-cache-dir psycopg2

RUN apk add --no-cache libxml2-dev libxslt-dev
RUN apk add --no-cache --virtual .pynacl_deps build-base libffi-dev

RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main openssl
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing gdal-dev
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing icu-libs

# INSTALL UWSGI
RUN apk add --no-cache uwsgi uwsgi-python3 uwsgi-python uwsgi-http uwsgi-corerouter uwsgi-stats_pusher_socket

# INSTALL wkhtmltopdf
RUN apk add --update --no-cache ttf-liberation
RUN apk add --no-cache wkhtmltopdf --repository http://dl-3.alpinelinux.org/alpine/edge/community/

# INSTALL PILLOW 
RUN apk add --no-cache \
    py3-pillow

# INSTALL BASH
RUN apk add --update --no-cache bash