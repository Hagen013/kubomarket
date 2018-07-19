import re

from django.shortcuts import redirect
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl import Search

from config.es_client import es_client
from config.search_patterns import generate_from_pattern
from core.models import ProductCard
from shop_cubes.serializers import CubesProductCardSerializer
from shop_cubes.models import CubesProductCard
from shop_cubes.serializers import CubesProductCardSerializer
from tasks.elastic import write_search_record


class SearchAPIView(APIView):

    block_size_standard = 3
    block_size_advanced = 7

    model = CubesProductCard
    serializer = CubesProductCardSerializer

    def get(self, request):
        query = request.GET.get('line', '')
        is_safe_mode = request.GET.get('safe', None)
        if settings.DEBUG is False:
            write_search_record(query, "SearchAPIView")

        search_body_standard = {
            'from': 0,
            'size': self.block_size_standard,
            'query': {
                "match": {
                    "name.autocomplete": query
                }
            }
        }
        search_body_advanced = generate_from_pattern(query)

        search_standard = Search(index='product_card', doc_type='product_card_index') \
            .from_dict(search_body_standard) \
            .using(es_client)
        search_advanced = Search(index='product_card', doc_type='product_card_index') \
            .from_dict(search_body_advanced) \
            .using(es_client)

        results_standard = list(map(lambda x: x['_source'], search_standard.execute().hits.hits))
        results_advanced = list(map(lambda x: x['_source'], search_advanced.execute().hits.hits))
        results_standard_pks = {result['id'] for result in results_standard}
        results_advanced = [
            result for result in results_advanced if result['id'] not in results_standard_pks
        ]

        results_standard_length = len(results_standard)
        results_advanced_legth = len(results_advanced)

        if results_standard_length < self.block_size_standard:
            difference = self.block_size_standard - results_standard_length
        else:
            difference = 0

        results_advanced_legth_max = self.block_size_advanced + difference
        if results_advanced_legth > results_advanced_legth_max:
            results_advanced = results_advanced[:results_advanced_legth_max]

        if is_safe_mode is None:
            return Response({
                'results_standard': results_standard,
                'results_advanced': results_advanced,
            })
        else:
            # !LIST а не SET как ранее для сохранения порядка релевантности
            results_standard_pks = [result['id'] for result in results_standard]
            results_advanced_pks = [result['id'] for result in results_advanced]

            results_standard = self.model.objects.filter(id__in=results_standard_pks)
            results_advanced = self.model.objects.filter(id__in=results_advanced_pks)

            results_standard = self.serializer(results_standard, many=True).data
            results_advanced = self.serializer(results_advanced, many=True).data

            return Response({
                'results_standard': results_standard,
            })


class SearchByCodeAPIView(APIView):

    def get(self, request):
        query = request.GET.get('line') or ''
        if settings.DEBUG is False:
            write_search_record.delay(query, "SearchByCodeAPIView")

        product = self.get_product(query)
        if product:
            results = CubesProductCardSerializer([product], many=True).data
            return Response({
                'results_standard': results,
                'results_advanced': []
            })
        else:
            return redirect('api:search:json-search')

    def get_product(self, query):
        pattern = re.compile(r'^[0-9]*$')
        try:
            code = int(pattern.findall(query)[0])
        except ValueError:
            return None
        vendor_code = "cubemarket-" + str(code)
        try:
            product = CubesProductCard.objects.get(vendor_code=vendor_code)
            return product
        except CubesProductCard.DoesNotExist:
            return None


class FacetesSearchAPIView(APIView):

    def get(self, request):
        slug = request.GET.get("slug")
        fields = set(request.GET.keys()).difference({'slug', slug})
        body = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {"is_in_stock": "true"}
                        }
                    ]
                }
            },
            "aggs": {
                "facet": {
                    "terms": {"field": slug, "size": 100000}
                }
            }
        }

        for field in fields:
            values = request.GET.get(field).split(',')
            body['query']['bool']['must'].append({
                "terms": {
                    field: values
                }
            })

        response = es_client.search(
            index="store",
            doc_type="product",
            body=body
        )

        return Response(response)
