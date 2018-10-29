from django.core.cache import cache

from celery.signals import beat_init
from celery.schedules import crontab
from config.celery import app

from cart.models import Order2
from shop_cubes.models import CubesProductCard as Product

@app.task
def inspect_orders():
    required_count = 6
    last_bought = set()

    for item in Order2.objects.all().order_by('-created_at')[:100]:
        if item.state == "доставка":
            items = list(item.data['cart']['items'].keys())
            for item in items:
                pk = item.split('__')[-1]
                try:
                    pk = int(pk)
                    last_bought.add(pk)
                except ValueError:
                    pass
            if len(last_bought) >= 6:
                last_bought = list(last_bought)[:6]
                break

    Product.objects.filter(recently_bought=True).update(
        recently_bought=False
    )

    Product.objects.filter(id__in=last_bought).update(
        recently_bought=True
    )
    



app.add_periodic_task(
    crontab(minute=0,  hour='*/12'),
    inspect_orders.s(),
    name='inspect_orders',
)