import json
import os

from unidecode import unidecode

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.cache import cache
from django.db import transaction
from django.db import IntegrityError
from django.template.defaultfilters import slugify

import pandas as pd
import numpy as np

from config.celery import app

from core.utils import slugify
from shop_cubes.models import CubesProductCard as ProductCard
from shop_cubes.models import CubesAttribute as Attribute
from shop_cubes.models import CubesAttributeValue as AttributeValue


@app.task
def generate_offers_file():
    FILE_PATH = settings.ADMIN_DOWNLOADS + 'data.xlsx'
    qs = ProductCard.objects.all().values(
        'name',
        'price',
        'purchase_price',
        'vendor_code',
        'vendor',
        'is_in_stock',
        'model'
    )
    df = pd.DataFrame(list(qs))
    df['is_in_stock'] = df['is_in_stock'].apply(int)
    df = df.reindex_axis(
        ['vendor_code', 'vendor', 'model', 'name', 'price', 'purchase_price', 'is_in_stock'], axis=1)
    writer = pd.ExcelWriter(FILE_PATH)
    df.to_excel(writer, 'Ostatki')
    writer.save()


@app.task
def process_uploaded_file(path):
    df = pd.read_excel(path)

    quantity = df.shape[0]
    progress_counter = 0
    progress = 0
    cache.set('controls_proceeding_upload_file_progress', progress)

    products_changed = 0
    products_not_found = 0
    price_changed = 0
    availability_changed = 0
    availability_changed_to_false = 0
    availability_changed_to_true = 0
    vendor_changed = 0
    name_changed = 0
    model_changed = 0
    purchase_price_changed = 0

    log_msgs = []

    with transaction.atomic():
        for index, row in df.iterrows():

            name = row['name']
            price = row['price']
            purchase_price = row['purchase_price']
            vendor_code = row['vendor_code']
            vendor = row['vendor']
            is_in_stock = bool(row['is_in_stock'])
            model = row['model']

            try:
                product = ProductCard.objects.get(vendor_code=vendor_code)
                product_changed = False

                if product.price != price:
                    difference = price - product.price
                    try:
                        percentage = round(difference / product.price, 2) * 100
                    except ZeroDivisionError:
                        percentage = 100
                    msg = "{0} price changed from {1} to {2} ({3}%)".format(
                        product.vendor_code,
                        product.price,
                        price,
                        percentage
                    )
                    log_msgs.append(msg)

                    product.price = price
                    price_changed += 1
                    product_changed = True

                if product.purchase_price != purchase_price:
                    difference = purchase_price - product.purchase_price
                    try:
                        percentage = round(difference / product.purchase_price, 2) * 100
                    except ZeroDivisionError:
                        percentage = 100
                    msg = "{0} purchase_price changed from {1} to {2} ({3}%)".format(
                        product.vendor_code,
                        product.purchase_price,
                        purchase_price,
                        percentage
                    )
                    log_msgs.append(msg)

                    product.purchase_price = purchase_price
                    purchase_price_changed += 1
                    product_changed = True

                if product.name != name:
                    msg = "{0} name changed {0} -> {2}".format(
                        product.vendor_code,
                        product.name,
                        name
                    )
                    log_msgs.append(msg)
                    
                    product.name = name
                    name_changed += 1
                    product_changed = True

                if product.vendor != vendor:
                    msg = "{0} vendor changed {1} -> {2}".format(
                        product.vendor_code,
                        product.vendor,
                        vendor
                    )
                    log_msgs.append(msg)
                    product.vendor = vendor
                    vendor_changed += 1
                    product_changed = True

                if product.is_in_stock is not is_in_stock:
                    msg = "{0} availability changed from {1} to {2}".format(
                        product.vendor_code,
                        product.is_in_stock,
                        is_in_stock
                    )
                    log_msgs.append(msg)
                    product.is_in_stock = is_in_stock
                    availability_changed += 1
                    product_changed = True
                    if is_in_stock:
                        availability_changed_to_true += 1
                    else:
                        availability_changed_to_false += 1

                if product.model != model:
                    msg = "{0} model changed from {1} to {2}".format(
                        product.vendor_code,
                        product.model,
                        model
                    )
                    log_msgs.append(msg)
                    product.model = model
                    model_changed += 1
                    product_changed = True

                if product_changed:
                    products_changed += 1
                    product.save()

            except ProductCard.DoesNotExist:
                products_not_found += 1

            progress_counter += 1
            progress = round(progress_counter / quantity, 2)
            cache.set('controls_proceeding_upload_file_progress', progress)
            test = cache.get('controls_proceeding_upload_file_progress')

    report_filename = settings.ADMIN_DOWNLOADS + 'report.txt'

    short_report = """
        Товаров изменено: {products_changed}
        Товаров не найдено: {products_not_found}
        Цен изменено: {price_changed}
        Оптовых цен изменено: {purchase_price_changed}
        Наличие изменено: {availability_changed}
        Наличие изменено на > ОТСУТСТВУЕТ: {availability_changed_to_false}
        Наличие изменено на > В НАЛИЧИИ: {availability_changed_to_true}
        Производитель изменен: {vendor_changed}
        Название изменено: {name_changed}
        Модель изменена: {model_changed}

    """.format(
        products_changed=products_changed,
        products_not_found=products_not_found,
        price_changed=price_changed,
        purchase_price_changed=purchase_price_changed,
        availability_changed=availability_changed,
        availability_changed_to_false=availability_changed_to_false,
        availability_changed_to_true=availability_changed_to_true,
        vendor_changed=vendor_changed,
        name_changed=name_changed,
        model_changed=model_changed
    )

    with open(report_filename, 'w') as fp:
        fp.write(short_report)
        for message in log_msgs:
            fp.write(message+'\n')

    report_data = {
        'products_changed': products_changed,
        'products_not_found': products_not_found,
        'price_changed': price_changed,
        'purchase_price_changed': purchase_price_changed,
        'availability_changed': availability_changed,
        'availability_changed_to_false': availability_changed_to_false,
        'availability_changed_to_true': availability_changed_to_true,
        'vendor_changed': vendor_changed,
        'name_changed': name_changed,
        'model_changed': model_changed,
    }
    return report_data


@app.task
def process_uploaded_attrs_file(path):
    df = pd.read_excel(path)
    log_msgs = []

    products_proceeded = 0
    attributes_values_proceeded = 0

    products_not_found = 0
    attributes_values_not_found = 0
    duplicate_attribute_values = 0

    invalid_vendor_code = 0
    invalid_slugs = 0

    product = None
    slugs = None

    def get_int_value_name(attribute, int_value):
        if attribute.name == 'Вес':
            name = str(int_value) + ' г.'
        elif attribute.name == 'Объем':
            name = str(int_value) + ' л.'
        else:
            name = str(int_value)
        return name

    for index, row in df.iterrows():
        # Trying to get a product
        if pd.isnull(row['vendor_code']):
            invalid_vendor_code += 1
            msg = "Invalid vendor_code at index :{index}".format(
                index=index
            )
            log_msgs.append(msg)
            continue

        # Trying to proceed the values
        if pd.isnull(row['slugs']):
            invalid_slugs += 1
            msg = "Invalid vendor_code at index: {index}".format(
                index=index
            )
            log_msgs.append(msg)
            continue
    
        vendor_code = row['vendor_code']
        try:
            product = ProductCard.objects.get(vendor_code=vendor_code)
            products_proceeded += 1
        except ObjectDoesNotExist:
            msg = "Product with vendor_code: {vendor_code} not found".format(
                vendor_code=vendor_code
            )
            log_msgs.append(msg)
            products_not_found += 1
            continue

        slugs = [slug.strip() for slug in row['slugs'].split('#')]
        for slug in slugs:
            value = None
            try:
                value = AttributeValue.objects.get(slug=slug)
            except ObjectDoesNotExist:
                if "__int__" in slug:
                    items = slug.split("__")
                    int_value = int(items[2])
                    attribute_key = "__int__" + items[3]
                    try:
                        attribute = Attribute.objects.get(key=attribute_key)
                    except ObjectDoesNotExist:
                        attribute is None
                    if attribute is not None:
                        value_name = get_int_value_name(attribute, int_value)
                        value = AttributeValue(
                            attribute=attribute,
                            attribute_type=attribute.attribute_type,
                            slug=slug,
                            name=value_name,
                            _int_value=int_value
                        )
                        try:
                            value.full_clean()
                            value.save()
                        except ValidationError:
                            print("Integer AttributeValue with slug: {slug} is not valid".format(
                                slug=slug
                            ))
                            log_msgs.append(msg)
                else:
                    msg = "AttributeValue with slug: {slug} not found".format(
                        slug=slug
                    )
                    log_msgs.append(msg)
                    attributes_values_not_found += 1

            if value is not None:
                attributes_values_proceeded += 1
                try:
                    product.add_attribute_value(value)
                except IntegrityError:
                    duplicate_attribute_values += 1
                    msg = "[DUPLICATE] Product {0} already has attribute value: {1}".format(
                        vendor_code,
                        slug
                    )
                    log_msgs.append(msg)

    report_data = {
        'products_proceeded': products_proceeded,
        'attributes_values_proceeded': attributes_values_proceeded,
        'products_not_found': products_not_found,
        'attributes_values_not_found': attributes_values_not_found,
        'duplicate_attribute_values': duplicate_attribute_values
    }

    short_report = """
    Товаров обработано: {products_proceeded}
    Товаров не найдено: {products_not_found}
    AttributeValue обработано: {attributes_values_proceeded}
    AttributeValue не найдено: {attributes_values_not_found}
    Дублирующихся значений: {duplicate_attribute_values}

    """.format(
        products_proceeded=products_proceeded,
        products_not_found=products_not_found,
        attributes_values_proceeded=attributes_values_proceeded,
        attributes_values_not_found=attributes_values_not_found,
        duplicate_attribute_values=duplicate_attribute_values
    )

    report_filename = settings.ADMIN_DOWNLOADS + 'report_products_attrs.txt'
    with open(report_filename, 'w') as fp:
        fp.write(short_report)
        for message in log_msgs:
            fp.write(message+'\n')

    os.remove(path)

    return report_data


@app.task
def upload_offers(filepath):
    """
    Функция загрузки новых товарных предложений из файла
    """
    df = pd.read_excel(filepath)
    duplicate_products = 0
    products_added = 0

    for index, row in df.iterrows():
        vendor_code = row['vendor_code']
        vendor = row['vendor']
        model = row['model']
        name = row['name']
        is_in_stock = bool(row['is_in_stock'])
        price = row['price']
        purchase_price = row['purchase_price']
        slug_body = name
        slug = slugify(slug_body)
        item_slug = slug + "/"

        try:
            product = ProductCard.objects.get(vendor_code=vendor_code)
            duplicate_products += 1
        except ProductCard.DoesNotExist:
            instance = ProductCard(
                vendor_code=vendor_code,
                vendor=vendor,
                model=model,
                name=name,
                is_in_stock=is_in_stock,
                price=price,
                purchase_price=purchase_price,
                slug=item_slug
            )
            try:
                instance.save(update_search=True)
                products_added += 1
            except IntegrityError:
                for count in range(1000):
                    try:
                        instance.slug = slug + '-' + str(count) + '/'
                        instance.save(update_search=True)
                        products_added += 1
                        break
                    except:
                        pass

    return {
        "duplicate_products": duplicate_products,
        "products_added": products_added,
    }

