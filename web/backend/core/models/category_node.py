from collections import OrderedDict

from django.db import models, transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

from ..db import WebPage, DisplayableManager, Named, Describable, TimeStamped
from ..db.base.fields import DisplayableURLField
from ..utils import disallowed_before_creation, DisallowedBeforeCreationException


class NodeManager(TreeManager):

    def rebuild(self):
        for node in self.get_queryset():
            node.set_depth()
            node.save()
        for node in self.get_queryset():
            node.set_inputs()
        root = self.get_queryset().get(_depth=0)
        for node in self.get_queryset().filter(_depth=1):
            node.add_input(root)
        for node in self.get_queryset():
            if node.has_inputs:
                node.parent = node.inputs.all().order_by('-scoring')[0]
                node.save()
        super(NodeManager, self).rebuild()
        for node in self.get_queryset():
            old_url = node.url
            new_url = node.get_graph_url()

            if node.id == 262:
                print(new_url)
        
            stored_node_exists = False
            try:
                stored_node = self.get_queryset().get(url=new_url)
                stored_node_exists = True
            except ObjectDoesNotExist:
                pass

            if stored_node_exists:
                pass
            else:
                node.url = new_url
            node.save()

            # Handling old outdated urls
            if old_url != node.url:
                try:
                    instance = node.outdated_url_class.objects.get(
                        url=old_url
                    )
                    instance.delete()
                except ObjectDoesNotExist:
                    pass
                instance = node.outdated_url_class(
                    node=node,
                    url=old_url
                )
                instance.save()

    def get_by_product(self, product_instance):
        if product_instance.pk:
            try:
                return self.get(id=self
                                .get_queryset()
                                .values('id')
                                .filter(attribute_values__in=product_instance
                                        .attribute_values
                                        .all())
                                .annotate(len_av=models.Count("id",
                                                              distinct=False)
                                          )
                                .order_by('-len_av', '-scoring')[0]['id'])
            except (IndexError, ObjectDoesNotExist):
                return self.get(slug='')
        else:
            raise DisallowedBeforeCreationException('product_instance must be creatied')

    def get_exact_node(self, values):
        if len(values) == 1:
            values = str(values).replace(",", "")
        elif len(values) == 0:
            return self.get_queryset().filter(level=0).order_by("id")
        query = """
        SELECT "shop_cubes_cubescategorynode"."id", COUNT("shop_cubes_cubescategorynodeattributevaluerelation"."attributevalue_id") AS "len_av"
        FROM "shop_cubes_cubescategorynode"
        INNER JOIN "shop_cubes_cubescategorynodeattributevaluerelation"
        ON ("shop_cubes_cubescategorynodeattributevaluerelation"."category_id"="shop_cubes_cubescategorynode"."id")
        INNER JOIN "shop_cubes_cubesattributevalue"
        ON ("shop_cubes_cubesattributevalue"."id"="shop_cubes_cubescategorynodeattributevaluerelation"."attributevalue_id")
        WHERE "shop_cubes_cubescategorynode"."id" NOT IN (
            SELECT "shop_cubes_cubescategorynode"."id"
            FROM "shop_cubes_cubescategorynode"
            INNER JOIN "shop_cubes_cubescategorynodeattributevaluerelation"
            ON ("shop_cubes_cubescategorynode"."id" = "shop_cubes_cubescategorynodeattributevaluerelation"."category_id")
            WHERE "shop_cubes_cubescategorynodeattributevaluerelation"."attributevalue_id" NOT IN {values}
            GROUP BY "shop_cubes_cubescategorynode"."id"
        )
        GROUP BY "shop_cubes_cubescategorynode"."id"
        ORDER BY "len_av" DESC, "shop_cubes_cubescategorynode"."scoring" DESC
        """.format(values=values)

        qs = self.raw(query)
        
        return qs


class NodePublicManager(NodeManager, DisplayableManager):

    def rebuild(self):
        raise Exception('NodePublicManager has no permission to use rebuild() method')


class CategoryNode(MPTTModel, WebPage, Named):

    class Meta:
        abstract = True

    objects = NodeManager()
    public = NodePublicManager()

    inputs_relation_class = None
    related_relation_class = None
    attributevalues_relation_class = None
    outdated_url_class = None

    product_card_class = None

    attribute_values = None
    # RELATIONS

    parent = None
    inputs = None
    outputs = None
    attribute_values = None

    # Fields
    _depth = models.PositiveIntegerField(
        default=0,
        verbose_name='глубина узла в графе'
    )

    # Methods:
    def get_url(self):
        return self.url

    @property
    def depth(self):
        return self._depth

    @property
    def has_inputs(self):
        return self.inputs.count() > 0

    @property
    def has_outputs(self):
        return self.outputs.count() > 0

    @property
    def is_detached(self):
        return self.get_root()._depth > 0

    @property
    def nav_nodes(self):
        return self.outputs.filter(is_published=True).order_by('-scoring')

    @property
    def gruped_nav_nodes(self):
        qs = self.inputs_relation_class.objects.filter(
            output_node=self,
            input_node__is_published=True
        ).select_related('input_node', 'group', 'added_attribute_value')\
            .order_by('group__order', '-input_node__scoring')

        result = OrderedDict()

        for i in qs:
            node = i.input_node
            node.added_attribute_value = i.added_attribute_value
            result[i.group] = result.get(i.group, []) + [node]
        return result

    @property
    def truncated_breadcrumbs(self):
        """
        'Рюкзаки женские городские повседневные' ->
        [{'title': 'Рюкзаки', 'url': 'ryukzak'},
        {'title': 'Городские', 'url': 'ryukzak/gorodskoj'},
        {'title': 'Женские', 'url': 'ryukzak/gorodskoj/zhenskij'},
        {'title': 'Повседневные', 'url': 'ryukzak/gorodskoj/zhenskij/povsednevnyj'}]
        """
        breadcrumbs = []
        ancestors = self.get_ancestors(include_self=True)
        breadcrumbs.append(
            {'title': ancestors[0].title, 'url': ancestors[0].url}
        )
        for i in range(1, len(ancestors)):
            title = ancestors[i].title.lower().replace(
                ancestors[i - 1].title.lower(), ''
            ).strip().capitalize()
            breadcrumbs.append({'title': title, 'url': ancestors[i].url})
        return breadcrumbs

    def get_graph_url(self):
        """
        Функция получения собственного графового URL:
        - применим только к не оторванным от общего графа узлам
        - для корректной работы должны быть прорисованы inputs графа и parent
        эталонного mptt-дерева
        """
        if self._depth == 0:
            return ''
        if self.is_detached:
            return self.url
        slugs_list = []
        slugs_set = set()
        ancestors = self.get_ancestors(include_self=True)
        for ancestor in ancestors:
            ancestor_values = ancestor.attribute_values.all()
            ancestor_slugs_set = set(map(lambda x: x.slug, ancestor_values))
            difference = ancestor_slugs_set.difference(slugs_set)
            difference_list = list(difference)
            slugs_set.update(difference)
            if len(difference_list) > 0:
                slugs_list.append(difference_list[0])
        return '/'.join(slugs_list) + '/'

    def set_depth(self):
        self._depth = self.get_depth()

    @disallowed_before_creation
    def get_depth(self):
        return self.attribute_values.count()

    def add_value(self, value):
        relation = self.attributevalues_relation_class(
            category=self,
            attributevalue=value
        )
        relation.save()

    def remove_value(self, value):
        relation = self.attributevalues_relation_class.get(
            category=self,
            attributevalue=value
        )
        relation.delete()

    def update_values(self, values):
        stored_values = self.attribute_values.all()
        stored_values_ids = {value.id for value in stored_values}
        values_ids = {value.id for value in values}
        ids_to_add = values_ids.difference(stored_values_ids)
        ids_to_delete = stored_values_ids.difference(values_ids)

        self.attributevalues_relation_class.objects.filter(
            category=self,
            attributevalue__id__in=ids_to_delete
        ).delete()

        values_to_add = [value for value in values if value.id in ids_to_add]
        for instance in values_to_add:
            relation = self.attributevalues_relation_class(
                category=self,
                attributevalue=instance
            )
            relation.save()


    @disallowed_before_creation
    def add_input(self, instance):
        """
        Предполагается что:
            self.attribute_values == added_attribute_value + instance.attribute_values
        """
        added_attribute_value = self.attribute_values.all().difference(instance.attribute_values.all())
        if added_attribute_value.count() != 1:
            raise ValueError("Numbers of added attribute_value not 1")
        relation = self.inputs_relation_class(
            output_node=instance,
            input_node=self,
            group=added_attribute_value[0].attribute.category_node_group,
            added_attribute_value=added_attribute_value[0]
        )
        relation.save()

    @disallowed_before_creation
    def set_inputs(self):
        self.inputs.clear()
        values = self.attribute_values.all()
        values_set = set(map(lambda x: x.slug, values))
        potential_inputs = self._meta.default_manager.filter(
            _depth=self._depth - 1,
            id__in=self
            ._meta.default_manager
            .values('id')
            .filter(attribute_values__in=values.values('id'))
            .annotate(len_av=models.Count("id", distinct=False))
            .filter(len_av=values.count() - 1)
            .values('id')
        )
        for node in potential_inputs:
            self.add_input(node)

    @property
    def products(self):
        if self.url == '':
            return self.product_card_class.objects.all()
        else:
            av = self.attribute_values.all()
            return self.product_card_class.objects.filter(
                id__in=self
                .product_card_class
                .objects.values('id')
                .filter(attribute_values__in=av)
                .annotate(len_av=models.Count("id", distinct=False))
                .filter(len_av=len(av)).values('id')
            )

    # Representation
    def __str__(self):
        return "CategoryNode: {0}".format(self.title)

    def __init__(self, *args, **kwargs):
        super(CategoryNode, self).__init__(*args, **kwargs)


class CategoryNodeOutdatedUrl(TimeStamped):

    node = None

    url = DisplayableURLField()

    class Meta:
        abstract = True
