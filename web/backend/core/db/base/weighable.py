from django.db import models


class Weighable(models.Model):

    class Meta:
        abstract = True

    weigh = models.PositiveIntegerField(
        verbose_name='Вес - кг',
        default=0
    )
