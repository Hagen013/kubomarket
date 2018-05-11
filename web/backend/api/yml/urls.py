from django.conf.urls import url, include

from .views import CubesYmlApiView

urls_yml = ([
    url(r'^cubes-yml\.xml/$',
        CubesYmlApiView.as_view(),
        name='cubes')
], 'yml')
