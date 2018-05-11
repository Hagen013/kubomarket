from rest_framework.views import APIView
from django.template.response import HttpResponse

from django.shortcuts import render
from django.utils import timezone
from django.core.cache import cache


from shop_cubes.models import CubesProductCard
from shop_cubes.models import CubesCategoryNode


class CubesYmlApiView(APIView):

    def get(self, request):
        categories = CubesCategoryNode.objects.all()
        products = CubesProductCard.public.all()

        context = {'date': timezone.now().strftime('%Y-%m-%d %H:%M'),
                   'categories': categories,
                   'products': products,
                   }

        pages_last_modify = max(CubesCategoryNode.objects.
                                latest('modified_at').modified_at,
                                CubesProductCard.objects.
                                latest('modified_at').modified_at
                                )

        cache_last_modify = cache.get('yml_cache_last_modify')

        if not cache_last_modify or (pages_last_modify > cache_last_modify):

            yml_response = render(request=request,
                                  template_name="api/yml.xml",
                                  context=context,
                                  )
            cache.set('yml_cache_last_modify', timezone.now())
            cache.set('yml.xml', yml_response)
        else:
            yml_response = cache.get('yml.xml')

        return HttpResponse(yml_response, content_type='text/xml')
