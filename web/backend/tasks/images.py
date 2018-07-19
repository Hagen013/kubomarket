from django.conf import settings
from django.db.models import Max
from django.db import transaction
from django.core.files.storage import FileSystemStorage

import pandas as pd
import numpy as np
import requests
from celery import states

from config.celery import app
from core.models import ProductCard
from shop_cubes.models import CubesProductCard
from shop_cubes.models import CubesProductAdditionalImage
from shop_cubes.models import CubesImagesRegisterRecord


@app.task
def synchronize_images(filepath):

    ALLOWED_FORMATS = set(('jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG'))

    df = pd.read_excel(filepath)
    df = df.sort_values(by=['scoring'], ascending=True)

    products_count = df['vendor_code'].unique().shape[0]
    products_set = set()

    invalid_urls_found = 0
    records_found = 0

    downloads_succeeded = 0
    downloads_failed = 0

    for index, row in df.iterrows():
        vendor_code = row['vendor_code']
        try:
            product = CubesProductCard.objects.get(vendor_code=vendor_code)
            products_set.add(vendor_code)
            urls = list(map(lambda url: url.strip(), row['urls'].split('#')))
            product_urls = []
            for url in urls:
                file_format = url.split('.')[-1]
                if file_format in ALLOWED_FORMATS:
                    product_urls.append(url)
                else:
                    invalid_urls_found += 1
            if len(product_urls) > 0:
                process_media_url.delay(product.id, product_urls)
        except CubesProductCard.DoesNotExist:
            pass


@app.task
def process_media_url(product_id, urls):
    failed = 0
    succeded = 0

    product = CubesProductCard.objects.get(id=product_id)
    for url in urls:
        try:
            record = CubesImagesRegisterRecord.objects.get(product=product, url=url)
        except CubesImagesRegisterRecord.DoesNotExist:
            file_name = url.split('/')[-1]
            download_path = '{0}original/{1}'.format(settings.MEDIA_BUFFER_PATH, file_name)
            response = requests.get(url, stream=True)
            status_code = response.status_code
            if status_code == 200:
                with open(download_path, 'wb') as fp:
                    for chunk in response.iter_content(1024):
                        fp.write(chunk)
                product.add_photo(download_path)
                record = CubesImagesRegisterRecord(
                    product=product,
                    url=url,
                )
                record.save()
                succeded += 1
            else:
                failed += 1
    return {
        "succeded": succeded,
        "failed": failed
    }


@app.task
def add_cubes_image_from_file(product_slug, image_file):
    product = CubesProductCard.objects.get(slug=product_slug)
    max_order = CubesProductAdditionalImage.objects.filter(
        product=product,
    ).aggregate(Max('order'))['order__max']
    if max_order is None:
        max_order = 0
    else:
        max_order += 1
    instance = CubesProductAdditionalImage(
        product=product,
        image=image_file,
        order=max_order
    )
    instance.save()


@app.task
def set_cubes_images_order():
    for product in CubesProductCard.objects.all():
        order = 0
        images = product.additional_images
        for image in images:
            image.order = order
            image.save()
            order += 1


@app.task
def check_main_image_files():
    for instance in ProductCard.objects.all():
        filepath = settings.MEDIA_ROOT + str(instance.image)
        try:
            fp = open(filepath)
            fp.close
        except FileNotFoundError:
            instance.image = instance.image.field.default
            instance.save()
        try:
            image_url = instance.image.url
            thumbnail_url = instance.thumbnail.url
        except OSError:
            instance.image = instance.image.field.default
            instance.save()


@app.task
def save_description_image(image_file, filename):
    path = settings.MEDIA_STORAGE_PATH + filename
    fs = FileSystemStorage()
    fs.save(path, image_file)


@app.task 
def wrap_description_images():
    from bs4 import BeautifulSoup
    qs = CubesProductCard.objects.all()
    with transaction.atomic():
        for instance in qs:
            if instance.description != "":
                soup = BeautifulSoup(instance.description, "html.parser")
                for img in soup.find_all("img"):
                    wrap = soup.new_tag("div")
                    wrap.attrs["class"] = "product-page__decription-image-wrap"
                    img.wrap(wrap)
                instance.description = str(soup)
                instance.save()
