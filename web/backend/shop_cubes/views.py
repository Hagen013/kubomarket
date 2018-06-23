from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView
from django.http import Http404

from core.viewmixins import DiggPaginatorViewMixin

from .models import (CubesCategoryNode,
                     CubesAttribute,
                     CubesAttributeValue,
                     CubesProductCard,
                     CubesCategoryNodeOutdatedUrl,
                    )


class CubesCategoryPageView(DiggPaginatorViewMixin, ListView):
    """
    Класс View для отображения страницы категории
    """

    template_name = "pages/category.html"
    context_object_name = "products"
    node_class = CubesCategoryNode
    outdated_node_class = CubesCategoryNodeOutdatedUrl

    allowed_sorting_options = {'-price': ('-price', 'id'),
                               'price': ('price', 'id'),
                               '-scoring': ('-scoring', 'id')}
    default_sorting_option = ('-scoring', 'id')

    def get(self, request, url, *args, **kwargs):
        self.category = self.get_category(url)
        return super(CubesCategoryPageView, self).get(self, request, *args, **kwargs)

    def get_category(self, url):
        try:
            category = self.node_class.objects.get(url=url)
        except self.node_class.DoesNotExist:
            try:
                category = self.outdated_node_class.objects.get(url=url)
            except self.outdated_node_class.DoesNotExist:
                raise Http404
        return category

    def get_queryset(self, *args, **kwargs):
        return self.category.products.filter(is_in_stock=True)

    def get_context_data(self, *args, **kwargs):
        context = super(CubesCategoryPageView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CubesProductPageView(TemplateView):

    template_name = 'pages/product.html'

    def get(self, request, slug, *args, **kwargs):
        self.product = self.get_product(slug)
        return super(CubesProductPageView, self).get(self, request, *args, **kwargs)

    def get_product(self, slug):
        try:
            return CubesProductCard.objects.get(slug=slug)
        except CubesProductCard.DoesNotExist:
            raise Http404

    def get_user_status(self):
        return self.request.user.is_superuser

    def get_context_data(self, *args, **kwargs):
        context = super(CubesProductPageView, self).get_context_data(**kwargs)
        context['product'] = self.product
        context['category'] = CubesCategoryNode.public.get_by_product(self.product)
        context['user_status'] = self.get_user_status()
        return context
