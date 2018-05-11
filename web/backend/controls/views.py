import os
from functools import wraps

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage

from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from config.celery import app

from tasks.controls import generate_offers_file, process_uploaded_file, \
    process_uploaded_attrs_file, upload_offers
from tasks.images import synchronize_images


def supersuer_method(fn):
    @wraps(fn)
    def wrapped(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return fn(self, request, *args, **kwargs)
        else:
            raise Http404
    return wrapped


class UploadsView(TemplateView):

    template_name = 'admin/uploads.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(UploadsView, self).get(request, *args, **kwargs)
        else:
            raise Http404


def download(request, path=settings.ADMIN_DOWNLOADS + 'data.xlsx'):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


class UploadFileAPIView(APIView):

    def get(self, request):
        if request.user.is_superuser:
            result_id = cache.get('process_offers_file_task_id')
            if result_id is not None:
                processing = True
                result = AsyncResult(result_id, app=app)
                is_ready = result.ready()
                progress = cache.get('controls_proceeding_upload_file_progress')
                state = result.state
            else:
                processing = False
                is_ready = False
                progress = 0
                state = 'EMPTY'
            return Response({
                'is_ready': is_ready,
                'processing': processing,
                'progress': progress,
                'state': state
            })
        else:
            raise Http404

    def post(self, request):
        if request.user.is_superuser:
            cache.set('process_offers_file_task_id', None)
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filepath = settings.ADMIN_UPLOADS + uploaded_file.name
            filename = fs.save(filepath, uploaded_file)
            result = process_uploaded_file.delay(filename)
            cache.set('process_offers_file_task_id', result.id)
            return Response({
                'acknowledged': True
            })
        else:
            raise Http404


class GenerateFileAPIView(APIView):

    def get(self, request):
        if request.user.is_superuser:
            result_id = cache.get('generate_offers_file_task_id')
            if result_id is not None:
                processing = True
                result = AsyncResult(result_id, app=app)
                is_ready = result.ready()
                state = result.state
            else:
                processing = False
                is_ready = False
                state = 'EMPTY'
            return Response({
                'is_ready': is_ready,
                'state': state
            })
        else:
            raise Http404

    def post(self, request):
        if request.user.is_superuser:
            cache.set('generate_offers_file_task_id', None)
            result = generate_offers_file.delay()
            cache.set('generate_offers_file_task_id', result.id)
            return Response({
                'acknowledged': True,
            })
        else:
            raise Http404


class AttributeValuesAPIView(APIView):

    @supersuer_method
    def get(self, request, *args, **kwargs):
        result_id = cache.get('process_uploaded_attrs_file_task_id')
        if result_id is not None:
            processing = True
            task = AsyncResult(result_id, app=app)
            is_ready = task.ready()
        else:
            processing = False
            is_ready = False
        if is_ready:
            results = task.get()
        else:
            results = {}
        return Response({
            'is_ready': is_ready,
            'processing': processing,
            'results': results
        })

    @supersuer_method
    def post(self, request, *args, **kwargs):
        cache.set('process_uploaded_attrs_file_task_id', None)
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filepath = settings.ADMIN_UPLOADS + uploaded_file.name
        filename = fs.save(filepath, uploaded_file)
        uploaded_file_url = fs.url(filename)
        result = process_uploaded_attrs_file.delay(filepath)
        cache.set('process_uploaded_attrs_file_task_id', result.id)
        return Response({
            'acknowledged': True,
        })


class ImagesSynchronizationAPIView(APIView):

    @supersuer_method
    def get(self, request, *args, **kwargs):
        result_id = cache.get('synchronize_images_taks_id')
        if result_id is not None:
            processing = True
            task = AsyncResult(result_id, app=app)
            is_ready = task.ready()
        else:
            processing = False
            is_ready = False
        if is_ready:
            results = task.get()
        else:
            results = {}
        return Response({
            'is_ready': is_ready,
            'processing': processing,
            'results': results
        })

    @supersuer_method
    def post(self, request, *args, **kwargs):
        cache.set('synchronize_images_task_id', None)
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filepath = settings.ADMIN_UPLOADS + uploaded_file.name
        filename = fs.save(filepath, uploaded_file)
        result = synchronize_images.delay(filename)
        cache.set('synchronize_images_taks_id', result.id)
        return Response({
            'acknowledged': True,
        })


class UploadOffersFileAPIView(APIView):

    @supersuer_method
    def get(self, request, *args, **kwargs):
        result_id = cache.get('upload_offers_task_id')
        if result_id is not None:
            processing = True
            task = AsyncResult(result_id, app=app)
            is_ready = task.ready()
        else:
            processing = False
            is_ready = False
        if is_ready:
            results = task.get()
        else:
            results = {}
        return Response({
            'is_ready': is_ready,
            'processing': processing,
            'results': results
        })
        return Response({
        })

    @supersuer_method
    def post(self, request, *args, **kwargs):
        cache.set('upload_offers_task_id', None)
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filepath = settings.ADMIN_UPLOADS + uploaded_file.name
        filename = fs.save(filepath, uploaded_file)
        result = upload_offers.delay(filename)
        cache.set('upload_offers_task_id', result.id)
        return Response({
            'acknowledged': True,
        }) 


class UploadOffersReportFileAPIView(APIView):

    filename = 'report.txt'

    @supersuer_method
    def get(self, request, *args, **kwargs):
        filename = settings.ADMIN_DOWNLOADS + self.filename
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/plain")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404


class UploadProductsAttributesReportFileAPIView(APIView):

    filename = 'report_products_attrs.txt'

    @supersuer_method
    def get(self, request, *args, **kwargs):
        filename = settings.ADMIN_DOWNLOADS + self.filename
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/plain")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404
