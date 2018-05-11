from django.db import models


class Dimensional(models.Model):

    """
    Габариты в сантиметрах
    """

    class Meta:
        abstract = True

    height = models.PositiveIntegerField(
        verbose_name='высота (см)',
        default=0
    )

    width = models.PositiveIntegerField(
        verbose_name='длина (см)',
        default=0
    )

    length = models.PositiveIntegerField(
        verbose_name='ширина (см)',
        default=0
    )

    @property
    def dimensions(self):
        if all((self.height, self.width, self.length)):
            return [self.height, self.width, self.length]
        else:
            return []

