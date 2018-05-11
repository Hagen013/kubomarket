#!/bin/bash

IMAGES=(
    "web_cube"
    "web_celery_cube"
    "web_flower_cube"
    "geo"
    "geo_celery"
    "geo_flower"
    "nginx_cube"
)

for image in ${IMAGES[@]}
do
    docker tag graphmarket/$image:latest graphmarket/$image:backup
    docker push graphmarket/$image:backup
done

sudo -u postgres -H -- pg_dump graph_market > /tmp/graph_market_beckup_db_dump;
sudo -u postgres -H -- pg_dump geo > /tmp/geo_beckup_db_dump;

mv -f /tmp/graph_market_beckup_db_dump ./db_dumps/graph_market_beckup_db_dump;
mv -f /tmp/geo_beckup_db_dump ./db_dumps/geo_beckup_db_dump;