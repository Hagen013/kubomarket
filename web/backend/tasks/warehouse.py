from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.conf import settings
from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from shop_cubes.models import CubesProductCard, CubesCategoryNode

FILEPATH = settings.YML_PATH + "warehouse.xml"


@app.task
def generate_warehouse_file():
    products = CubesProductCard.objects.all()
    categories = CubesCategoryNode.objects.all()
    date = now().astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M')

    context = {
        'date': date,
        'categories': categories,
        'products': products,
        'get_product_category': lambda product: CubesCategoryNode.public.get_by_product(product)
    }

    xml_raw = render_to_string(
        template_name="api/warehouse.xml",
        context=context
    )

    with open(FILEPATH, "w") as fp:
        fp.write(xml_raw)


app.add_periodic_task(
    crontab(minute=0,  hour='*/2'),
    generate_warehouse_file.s(),
    name='generate_warehouse_file',
)


@beat_init.connect
def configure_workers(**kwargs):
    import os.path
    if not os.path.isfile(FILEPATH):
        generate_warehouse_file.delay()
