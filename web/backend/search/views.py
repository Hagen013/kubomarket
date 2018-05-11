import re

from django.conf import settings
from django.views.generic import ListView, TemplateView
from django.http import Http404
from django.shortcuts import redirect

from digg_paginator import DiggPaginator
from elasticsearch_dsl import Search

from config.es_client import es_client
from config.search_patterns import generate_from_pattern
from shop_cubes.models import CubesProductCard, CubesCategoryNode
from tasks.elastic import write_search_record


class ElasticSearchQuery(object):

    def __init__(self, body, index, doc_type, es_client, page_size):
        self._body = body
        self._index = index
        self._doc_type = doc_type
        self._es_client = es_client
        self._page_size = page_size
        search = Search(index=index, doc_type=doc_type) \
            .from_dict(self._body) \
            .using(es_client)
        self._results = search.execute()

    def __len__(self):
        return self._results.hits.total

    def __getitem__(self, key):
        self._body['from'] = key.start
        self._body['size'] = self._page_size
        search = Search(index=self._index, doc_type=self._doc_type) \
            .from_dict(self._body) \
            .using(self._es_client)
        return search.execute().hits.hits


class ElastiListView(TemplateView):

    query_kwarg = 'line'
    index = None
    doc_type = None

    paginator_class = DiggPaginator
    page_kwarg = 'page'
    paginate_by = 24
    paginate_orphans = 0
    paginate_allow_empty_first_page = True
    paginate_body = 5
    paginate_padding = 2
    paginate_margin = 2
    paginate_tail = 1

    model = None
    context_object_name = 'object_list'

    def get(self, request, *args, **kwargs):
        self.client_query = kwargs.get('line') or request.GET.get(self.query_kwarg) or ''
        if settings.DEBUG is False:
            write_search_record.delay(self.client_query, "ElastiListView")
        self.search_body = self.get_search_body()
        self.query = ElasticSearchQuery(
            self.search_body, self.index, self.doc_type, es_client, self.paginate_by)
        return super(ElastiListView, self).get(request, *args, **kwargs)

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        return self.paginator_class(queryset,
                                    per_page,
                                    orphans=self.paginate_orphans,
                                    allow_empty_first_page=self.paginate_allow_empty_first_page,
                                    body=self.paginate_body,
                                    padding=self.paginate_padding,
                                    margin=self.paginate_margin,
                                    tail=self.paginate_tail,
                                    **kwargs
                                    )

    def get_search_body(self):
        raise NotImplementedError(
            'get_search_body method must be implemented by a subclass of ElastiListView'
        )

    def get_queryset(self, search_results):
        uuids = []
        mapping = {}
        for result in search_results:
            uuid = int(result['_source']['id'])
            mapping[uuid] = result['_score']
            uuids.append(uuid)
        qs = self.model.objects.filter(id__in=uuids)
        return sorted(qs, key=lambda instance: mapping[instance.id], reverse=True)

    def paginate_search(self, query, page_size):
        paginator = self.get_paginator(query, self.paginate_by)
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': force_text(e),
            })

    def get_context_data(self, **kwargs):
        paginator, page, search_results, is_paginated = self.paginate_search(self.query, self.paginate_by)
        queryset = self.get_queryset(search_results)
        context = {
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            self.context_object_name: queryset
        }
        context['query'] = self.client_query
        return context


class SearchResultsView(ElastiListView):

    template_name = 'pages/search.html'
    index = 'product_card'
    doc_type = 'product_card_index'

    model = CubesProductCard
    context_object_name = 'products'

    def get_search_body(self):
        return generate_from_pattern(self.client_query)


class SearchByCodeView(TemplateView):

    template_name = 'pages/cubes/product.html'

    query_kwarg = 'line'

    def get(self, request, *args, **kwargs):
        client_query = kwargs.get('line') or request.GET.get(self.query_kwarg) or ''
        if settings.DEBUG is False:
            write_search_record.delay(client_query, "SearchByCodeView")
        product = self.get_product(client_query)
        if product:
            return redirect('cubes:product', slug=product.slug)
        else:
            return redirect('search:results', line=client_query)

    def get_product(self, query):
        pattern = re.compile(r'b-247-(\d*).*$')
        code = int(pattern.findall(query)[0])
        try:
            product = CubesProductCard.objects.get(id=code)
            return product
        except CubesProductCard.DoesNotExist:
            return None
