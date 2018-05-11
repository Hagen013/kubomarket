from rest_framework.views import APIView
from django.template.response import HttpResponse

from django.shortcuts import render
from django.utils import timezone
from django.core.cache import cache


from shop_cubes.models import CubesProductCard


class YmlApiView(APIView):

    def get(self, request):
        cubes = CubesProductCard.objects.all()

        context = {'date': timezone.now().strftime('%Y-%m-%d %H:%M'),
                   'cubes': cubes,
                   }

        pages_last_modify = CubesProductCard.objects.latest('modified_at').modified_at

        cache_last_modify = cache.get('my-warehouse-yml_cache_last_modify')

        if not cache_last_modify or (pages_last_modify > cache_last_modify):

            yml_response = render(request=request,
                                  template_name="myWarehouse/yml.xml",
                                  context=context,
                                  )
            cache.set('my-warehouse-yml_cache_last_modify', timezone.now())
            cache.set('yml.xml', yml_response)
        else:
            yml_response = cache.get('yml.xml')

        return HttpResponse(yml_response, content_type='text/xml')
