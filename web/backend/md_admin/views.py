from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import redirect

from rest_framework.views import APIView


class AdminTemplateView(TemplateView):
    
    template_name = 'md-admin/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(AdminTemplateView, self).get(request, *args, **kwargs)
        else:
            return redirect("md-admin:login")


class DownloadFileAPIView(APIView):
    """
    Базовый класс APIView для обработки запросов с клиента на формирование
    файла по celery-таску и отдачи сообщений о статусе работы таска
    """
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class UploadFileAPIView(APIView):
    """
    Базовый класс APIView для обработки файлов с клиента, последующей
    его обработки в celery-таске и отдачи сообщений о статусе работы таска
    """
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class AdminLoginView(TemplateView):

    template_name = 'md-admin/login.html'

    def get(self, request, *args, **kwargs):
        return super(AdminLoginView, self).get(self, request, *args, **kwargs)