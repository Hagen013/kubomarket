FROM graphmarket/base_alpine:latest

# INSTALL PILLOW 
RUN apk add --no-cache \
    py3-pillow

# INSTALL REQUIREMENTS
COPY  web/requirements/base.txt base.txt
COPY  web/requirements/production.txt production.txt
COPY  web/requirements/flower.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# INSTALL BASH
RUN apk add --update --no-cache bash

# COPY ENTRYPOINT AND CODE
COPY web /web
COPY  compose/web_flower_cube/entrypoint.sh entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nobody

ENTRYPOINT ["/entrypoint.sh"]
