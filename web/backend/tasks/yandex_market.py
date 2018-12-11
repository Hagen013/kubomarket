from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.conf import settings
from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from shop_cubes.models import CubesProductCard, CubesCategoryNode

CUBES_YML_FILE = settings.YML_PATH + "cubes-yml.xml"


@app.task
def generate_yml_file():
    products = CubesProductCard.public.all()
    categories = CubesCategoryNode.objects.all()
    date = now().astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M')

    context = {'date': date,
               'categories': categories,
               'products': products,
               'get_product_category': lambda product: CubesCategoryNode.public.get_by_product(product)
               }

    xml_raw = render_to_string(template_name="api/yml.xml",
                               context=context)

    with open(CUBES_YML_FILE, "w") as fp:
        fp.write(xml_raw)


app.add_periodic_task(
    crontab(minute="*/30"),
    generate_yml_file.s(),
    name='generate_yml_file',
)


@beat_init.connect
def configure_workers(**kwargs):
    import os.path
    if not os.path.isfile(CUBES_YML_FILE):
        generate_yml_file.delay()
