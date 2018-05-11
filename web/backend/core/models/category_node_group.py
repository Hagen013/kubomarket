from ..db import Named, Describable, Orderable


class CategoryNodeGroup(Named, Describable, Orderable):
    """
    Группа категорий - связывается с категорией через значеие атрибута и инпут-таблицу
    CategoryNodeInputRelation.
    """
    class Meta:
        abstract = True
        verbose_name = 'Группа атрибута'
        verbose_name_plural = 'Группа атрибутов'

    attribute = None

    def __str__(self):
        return "CategoryNodeGroup: {}".format(self.name)
