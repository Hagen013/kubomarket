from shop_cubes.models import CubesCategoryNode
from config.celery import app
from celery.schedules import crontab


@app.task
def tree_rebuild():
    CubesCategoryNode.objects.rebuild()

app.add_periodic_task(
    crontab(minute=0,  hour='*/12'),
    tree_rebuild.s(),
    name='tree_rebuild',
)
