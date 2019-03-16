import json

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from urllib.parse import urlencode

from jinja2 import Environment

from shop_cubes.models import CubesCategoryNode
from .constants import links_mapping


def url_replace(querystring, kwargs):
    query = querystring.dict()
    query.update(kwargs)
    return urlencode(query)


def update_pagination(querystring, kwargs):
    query = querystring.dict()
    page = kwargs.get('page')
    if page == 1:
        kwargs.pop('page')
        query.pop('page')
    query.update(kwargs)
    if len(query.keys()) > 0:
        return "?" + urlencode(query)
    return ""


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


def format_time(date):
    formated_date = date.strftime("%Y.%m.%d")
    return formated_date

def check_inclusion(item_values, node_values):
    return len(node_values.difference(set(item_values))) == 0


def values_filter(values):
    output = ""
    keys = links_mapping.keys()
    length = len(values)
    count = 1
    for value in values:
        if value.name in keys:
            item = "<a href={url}>{text}</a>".format(
                url=links_mapping[value.name],
                text=value.name
            )
        else:
            item = "{text}".format(text=value.name)
        if count == length:
            pass
        else:
            item += ', '
        count += 1
        output += item
    return output

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'url_replace': url_replace,
        'to_json': to_json,
        'escape_quotes': escape_quotes,
        'rating_stars': rating_stars,
        'format_time': format_time,
        'update_pagination': update_pagination,
        'values_filter': values_filter
    })
    return env
