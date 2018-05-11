from django.conf.urls import url

from .views import UploadsView, GenerateFileAPIView, download,\
    UploadFileAPIView, AttributeValuesAPIView,\
    ImagesSynchronizationAPIView, UploadOffersFileAPIView,\
    UploadOffersReportFileAPIView, UploadProductsAttributesReportFileAPIView

urlpatterns = [
    url(r'^$', UploadsView.as_view(), name='main'),
    url(r'^download/status/$', GenerateFileAPIView.as_view(), name='download-status'),
    url(r'^download/$', download, name='download'),
    url(r'^upload/$', UploadFileAPIView.as_view(), name='upload'),
    url(r'^attrbiute-values/upload/$', AttributeValuesAPIView.as_view(), name='av-upload'),
    url(r'^images-sync/$', ImagesSynchronizationAPIView.as_view(), name='images-sync'),
    url(r'^upload-offers/$', UploadOffersFileAPIView.as_view(), name='upload-offers'),
    url(r'^upload-offers/report/$', UploadOffersReportFileAPIView.as_view(), name='upload-offers-report'),
    url(r'^upload-attrs/report/$',
        UploadProductsAttributesReportFileAPIView.as_view(),
        name='upload-attrs-report'),
]
