from django.conf.urls import url, include

from .views import CubesAdditionalImageUploadAPIView, CubesAdditionalImageAPIView


urls_images = ([
    url(r'upload/', CubesAdditionalImageUploadAPIView.as_view()),
    url(r'^(?P<image_id>(([\d]+)))/$', CubesAdditionalImageAPIView.as_view())
])
