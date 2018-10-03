import json

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from urllib.parse import urlencode

from jinja2 import Environment

from shop_cubes.models import CubesCategoryNode


def url_replace(querystring, kwargs):
    query = querystring.dict()
    query.update(kwargs)
    return urlencode(query)


def to_json(value):
    return json.dumps(value)


def escape_quotes(value):
    return value.replace("'", "")

def rating_stars(scoring):
    template = ""
    main = int(scoring/2)
    remain = scoring % 2
    empty_positions = 5 - main
    for i in range(main):
        template += '<div class="star star_full"></div>'
    if remain > 0.49:
        empty_positions -= 1
        template += '<div class="star star_half"></div>'
    for i in range(empty_positions):
        template += '<div class="star star_hollow"></div>'
    return template


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'url_replace': url_replace,
        'to_json': to_json,
        'escape_quotes': escape_quotes,
        'rating_stars': rating_stars
    })
    return env


def check_inclusion(item_values, node_values):
    return len(node_values.difference(set(item_values))) == 0
