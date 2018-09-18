FROM graphmarket/base_alpine:latest
RUN apk add --no-cache gcc
RUN apk add --no-cache libxml2-dev libxslt-dev
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

# INSTALL UWSGI
RUN apk add --no-cache uwsgi uwsgi-python3 uwsgi-python uwsgi-http uwsgi-corerouter uwsgi-stats_pusher_socket

# INSTALL PILLOW 
RUN apk add --no-cache \
    py3-pillow

RUN apk add --no-cache wkhtmltopdf

# INSTALL REQUIREMENTS
COPY  web/requirements/base.txt base.txt
COPY  web/requirements/production.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# INSTALL BASH
RUN apk add --update --no-cache bash

# COPY ENTRYPOINT AND CODE
COPY  web /web
COPY  compose/web_cube/uwsgi.ini uwsgi.ini
COPY  compose/web_cube/entrypoint.sh entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/entrypoint.sh"]