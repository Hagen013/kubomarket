import json

from django.contrib.staticfiles.storage import staticfiles_storage
# from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse
from urllib.parse import urlencode

from jinja2 import Environment

from shop_cubes.models import CubesCategoryNode


def url_replace(querystring, kwargs):
    query = querystring.dict()
    query.update(kwargs)
    return urlencode(query)


def to_json(value):
    return json.dumps(value)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'url_replace': url_replace,
        'to_json': to_json
    })
    return env


def check_inclusion(item_values, node_values):
    return len(node_values.difference(set(item_values))) == 0
