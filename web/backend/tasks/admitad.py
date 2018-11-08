from django.template.loader import render_to_string
from django.utils.timezone import now, pytz
from django.conf import settings
from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from cart.models import Order2

FILEPATH = settings.YML_PATH + "admitad.xml"


@app.task
def generate_admitad_file():
    qs = Order2.objects.filter(cpa__contains={'networks': ['admitad',]})[:500]
    context = {
                'orders': qs,
               }

    xml_raw = render_to_string(
        template_name="api/admitad.xml",
        context=context
    )

    with open(FILEPATH, "w") as fp:
        fp.write(xml_raw)


app.add_periodic_task(
    crontab(minute=0,  hour='*/6'),
    generate_admitad_file.s(),
    name='generate_admitad_file',
)


@beat_init.connect
def configure_workers(**kwargs):
    import os.path
    if not os.path.isfile(FILEPATH):
        generate_admitad_file.delay()
