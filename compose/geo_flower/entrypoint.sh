#!/bin/bash
set -e
cmd="$@"

function postgres_ready(){
python3 << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname='$POSTGRES_DATABASE', user='$POSTGRES_USER', password='$POSTGRES_PASSWORD', host='$POSTGRES_HOST')
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

function redis_ready(){
python3 << END
import redis
import sys
rs = redis.Redis('redis')
try:
    response = rs.client_list()
except redis.ConnectionError:
    sys.exit(-1)
sys.exit(0)
END
}

function rabbit_ready(){
python3 << END
from kombu import Connection
import sys
rabbit_url = 'amqp://$RABBIT_USER:$RABBIT_PASS@$RABBIT_HOSTNAME/$RABBIT_VHOST'
conn = Connection(rabbit_url)
try:
    conn.connect()
except:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - continuing..."

until redis_ready; do
  >&2 echo "Redis is unavailable - sleeping"
  sleep 1
done
>&2 echo "Redis is up - continuing..."

until rabbit_ready; do
  >&2 echo "Rabbit is unavailable - sleeping"
  sleep 1
done
>&2 echo "Rabbit is up - continuing..."

>&2 cd geo/backend
>&2 celery -A config flower --url_prefix=$FLOWER_URL_PREFIX --basic_auth=$FLOWER_ADMIN:$FLOWER_PASSWORD


exec $cmd
