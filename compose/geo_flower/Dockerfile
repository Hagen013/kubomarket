FROM graphmarket/base_alpine:latest
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

# INSTALL REQUIREMENTS
COPY  geo/requirements/base.txt base.txt
COPY  geo/requirements/production.txt production.txt
COPY  geo/requirements/flower.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


# INSTALL BASH
RUN apk add --update --no-cache bash

# COPY ENTRYPOINT AND CODE
COPY geo /geo
COPY  compose/geo_flower/entrypoint.sh entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nobody

ENTRYPOINT ["/entrypoint.sh"]
