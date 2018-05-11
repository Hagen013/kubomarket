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
    docker pull graphmarket/$image:backup
    docker tag  graphmarket/$image:backup graphmarket/$image:latest
done


sudo -u postgres -H -- psql -c "DROP DATABASE IF EXISTS graph_market;"
sudo -u postgres -H -- psql -c "CREATE DATABASE graph_market;"
sudo -u postgres -H -- psql -c "GRANT ALL PRIVILEGES ON DATABASE graph_market TO graph_market_admin;"

sudo -u postgres -H -- psql -c "DROP DATABASE IF EXISTS geo;"
sudo -u postgres -H -- psql -c "CREATE DATABASE geo;"
sudo -u postgres -H -- psql -c "GRANT ALL PRIVILEGES ON DATABASE geo TO geo_admin;"

sudo -u postgres psql graph_market < ./db_dumps/graph_market_beckup_db_dump;
sudo -u postgres psql geo < ./db_dumps/geo_beckup_db_dump;
