from django.db import models


class Orderable(models.Model):
    """
    Имеющее порядок
    """

    class Meta:
        abstract = True

    order = models.IntegerField(
        default=0,
        verbose_name='порядок'
    )
