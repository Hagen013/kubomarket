FROM madnight/docker-alpine-wkhtmltopdf

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    build-base \
    libffi-dev \
    && pip3 install --upgrade pip \
    && pip3 install numpy \
    && pip3 install pandas \
    && pip3 install --no-cache-dir psycopg2

RUN apk add --no-cache libxml2-dev libxslt-dev
RUN apk add --no-cache --virtual .pynacl_deps build-base libffi-dev


# INSTALL UWSGI
RUN apk add --no-cache uwsgi uwsgi-python3 uwsgi-python uwsgi-http uwsgi-corerouter uwsgi-stats_pusher_socket

# INSTALL PILLOW 
RUN apk add --no-cache \
    py3-pillow

# INSTALL BASH
RUN apk add --update --no-cache bash
