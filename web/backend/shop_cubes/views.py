import json
from collections import defaultdict

from django.views.generic import TemplateView, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import redirect
from django.db import connection
from django.db.models import Q
from django.http import Http404

from core.viewmixins import DiggPaginatorViewMixin
from .models import (CubesCategoryNode,
                     CubesAttribute,
                     CubesAttributeValue,
                     CubesProductCard,
                     CubesCategoryNodeOutdatedUrl,
                     CubesCategoryNodeGroup)

import django_filters
from django_filters import Filter
from django_filters.fields import Lookup


class ListFilter(Filter):

    def filter(self, qs, value):
        value_list = value.split(',')
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))


class ProductFilter(django_filters.FilterSet):

    price = django_filters.NumberFilter()
    price__gte = django_filters.NumberFilter(name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(name='price', lookup_expr='lte')
    vendor = ListFilter(name='vendor')

    class Meta:
        model = CubesProductCard
        exclude = ['image', 'thumbnail']


class CubesIndexPageView(TemplateView):

    template_name = 'pages/cubes/index.html'


class CubesProductPageView(TemplateView):

    template_name = 'pages/cubes/product.html'

    def get(self, request, *args, **kwargs):
        self.product = self.get_product()
        return super(CubesProductPageView, self).get(self, request, *args, **kwargs)

    def get_product(self):
        slug = self.kwargs.get('slug')
        try:
            return CubesProductCard.objects.get(slug=slug)
        except CubesProductCard.DoesNotExist:
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context = super(CubesProductPageView, self).get_context_data(**kwargs)
        context['product'] = self.product
        context['category'] = CubesCategoryNode.public.\
            get_by_product(self.product)
        return context


class CubesCategoryPageView(DiggPaginatorViewMixin, ListView):

    template_name = 'pages/cubes/category.html'
    context_object_name = 'products'

    node_class = CubesCategoryNode
    product_class = CubesProductCard
    filter_class = ProductFilter
    attribute_class = CubesAttribute
    value_class = CubesAttributeValue

    redirect_to_old_record = False
    outdated_node_class = CubesCategoryNodeOutdatedUrl

    paginate_by = 48

    allowed_sorting_options = {'-price': ('-price', 'id'),
                               'price': ('price', 'id'),
                               '-scoring': ('-scoring', 'id')}
    nonfilter_options = {"sort_by", "price__gte", "price__lte", "incomplete"}
    default_sorting_option = ('-scoring', 'id')

    def get(self, request, *args, **kwargs):
        self.category = self.get_category()
        querylength = len(request.GET.keys())
        if querylength > 0:
            self.exact_category = self.get_exact_category(request)
            if self.category.id != self.exact_category.id:
                redirect_queryparams = self.get_redirect_queryparams(self.exact_category)
                return custom_redirect('category', self.exact_category.url, **redirect_queryparams)
        self.is_admin = self.check_permissions(request)
        return super(CubesCategoryPageView, self).get(self, request, *args, **kwargs)

    def get_category(self, *args, **kwargs):
        url = self.kwargs.get('url')
        try:
            category = self.node_class.objects.get(url=url)
        except ObjectDoesNotExist:
            try:
                url_record = self.outdated_node_class.objects.get(url=url)
                category = url_record.node
                self.redirect_to_old_record = True
            except self.outdated_node_class.DoesNotExist:
                raise Http404
        return category

    def get_exact_category(self, request, *args, **kwargs):
        added_values = set()
        removed_values = set()
        self.queryparams = request.GET.dict()
        self.attrs_set = set(map(lambda x: x["key"], CubesAttribute.objects.all().values("key")))

        fields = list(filter(lambda x: x in self.attrs_set, self.queryparams))
        removed_fields = list(filter(lambda x: x[1:] in self.attrs_set, self.queryparams))

        for field in fields:
            values = {int(x) for x in self.queryparams.pop(field).split(',')}
            added_values.update(values)
        for field in removed_fields:
            values = {int(x) for x in self.queryparams.pop(field).split(',')}
            removed_values.update(values)

        category_values = {x['id'] for x in self.category.attribute_values.all().values('id')}
        self.search_values = category_values.difference(removed_values).union(added_values)
        exact_nodes = self.node_class.objects.get_exact_node(tuple(self.search_values))
        try:
            exact_node = exact_nodes[0]
        except IndexError:
            exact_node = self.category.get_root()
        return exact_node

    def get_redirect_queryparams(self, node):
        queryparams = defaultdict(list)
        values = node.attribute_values.values("id").all()
        values_set = {value["id"] for value in values}
        difference = self.search_values.difference(values_set)
        if len(difference) > 0:
            query_values = self.value_class.objects.filter(id__in=difference)
        else:
            query_values = []

        for value in query_values:
            queryparams[value.attribute.key].append(value.id)

        for key, value in self.queryparams.items():
            queryparams[key].append(value)

        return queryparams

    def check_permissions(self, request, *args, **kwargs):
        return request.user.is_staff

    def get_filters(self, *args, **kwargs):
        filters = CubesAttribute.objects.filter(
            Q(is_default_filter=True) | Q(filter_values__in=self.node_values)).order_by("-order")
        return filters

    def get_default_queryset(self, *args, **kwargs):
        fields = list(filter(lambda x: x in self.attrs_set, self.request.GET))
        queryparams = self.request.GET.dict()

        if len(fields) > 0:
            for key, values in queryparams.items():
                if key not in self.nonfilter_options:
                    values = values.split(",")
                    values = list(map(lambda x: int(x), values))
                    queryparams[key] = values

            for value in self.category.attribute_values.all():
                key = value.attribute.key
                if key in queryparams.keys():
                    queryparams[key].append(value.id)
                else:
                    queryparams[key] = [value.id]

            qs = self.product_class.objects.filter(is_in_stock=True)
            for key, values in queryparams.items():
                if key in self.attrs_set:
                    qs = qs.filter(attribute_values__in=values)
        else:
            qs = self.category.products

        qs = qs.filter(is_in_stock=True)

        qs = self.filter_class(
            self.request.GET,
            queryset=qs
        ).qs

        return qs

    def get_queryset(self, *args, **kwargs):
        sorting_option = self.request.GET.get('sort_by')
        sort_by = self.allowed_sorting_options.get(sorting_option, self.default_sorting_option)
        if self.request.user.is_staff:
            show_incomplete = self.request.GET.get('incomplete', None)
            self.is_admin = True
            if show_incomplete is None:

                qs = self.get_default_queryset(*args, **kwargs).annotate(
                    count=Count('attribute_values')).order_by('scoring', 'count')

            else:
                qs = self.get_default_queryset(*args, **kwargs).order_by(*sort_by)
        else:
            qs = self.get_default_queryset(*args, **kwargs).order_by(*sort_by)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(CubesCategoryPageView, self).get_context_data(**kwargs)
        context['category'] = self.category

        self.node_values = CubesAttributeValue.objects.filter(categories=self.category)
        node_values_set = {str(value.id) for value in self.node_values}
        print("\n\n\n")
        print(node_values_set)
        print("\n\n\n")
        node_values = list(map(lambda x: {"key": x.attribute.key, "id": x.id}, self.node_values))
        node_values = json.dumps(node_values)
        context["node_values"] = str(node_values)
        context["node_values_set"] = node_values_set

        filters = self.get_filters()
        context['filters'] = filters

        context['is_admin'] = self.is_admin
        return context


def custom_redirect(url_name, *args, **kwargs):
    from django.urls import reverse
    import urllib.parse
    from django.http import HttpResponseRedirect
    url = reverse(url_name, args=args)
    params = list(
        map(lambda x: "{key}={values}".format(key=x, values=",".join([str(i) for i in kwargs[x]])), kwargs.keys()))
    params = '&'.join(params)
    return HttpResponseRedirect(url + "?%s" % params)
