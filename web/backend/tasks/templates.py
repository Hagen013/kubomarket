from django.template.loader import render_to_string
from django.conf import settings

from jinja2 import Template
from config.celery import app

from shop_cubes.models import CubesCategoryNode as Node
from shop_cubes.models import CubesAttribute as Attribute
from shop_cubes.models import CubesAttributeValue as Value

@app.task
def generate_static_navigation():
    TEMPLATE_OUTPUT_PATH = settings.TEMPLATES[1]['DIRS'][0]

    nav_nodes = [
        
    ]

    node = Node.objects.get(url="kuby-nxnxn/")
    nav_nodes.append({
        "name": "Стандартные кубы",
        "id": node.id,
        "href": node.url,
        "childs": node.childs.all().order_by("scoring")
    })
    childs = nav_nodes[-1]["childs"]
    for child in childs:
        child.name = "Кубы" + child.name
    childs = [child for child in childs if child.products.count() > 0]
    nav_nodes[-1]["childs"] = childs

    node = Node.objects.get(url="nestandartnie/")
    nav_nodes.append({
        "name": "Нестандартные кубы",
        "id": node.id,
        "href": node.url,
        "childs": node.childs.all().order_by("scoring")
    })
    childs = nav_nodes[-1]["childs"]
    childs = [child for child in childs if child.products.count() > 0]
    nav_nodes[-1]["childs"] = childs

    nav_nodes.append({
        "name": "По бренду",
        "id": None,
        "href": None,
        "childs": Node.objects.filter(attribute_values__in=Attribute.objects.get(name="Бренд").values.all()).order_by("scoring")
    })
    childs = nav_nodes[-1]["childs"]
    childs = [child for child in childs if child.products.count() > 0]
    nav_nodes[-1]["childs"] = childs

    node = Node.objects.get(url="tajmery-i-maty/")
    nav_nodes.append({
        "name": "Таймеры и маты",
        "id": node.id,
        "href": node.url,
        "childs": []
    })

    node = Node.objects.get(url="smazki/")
    nav_nodes.append({
        "name": "Смазки",
        "id": node.id,
        "href": node.url,
        "childs": []
    })

    context = {
        "nodes": nav_nodes
    }

    vertical_nav = render_to_string("navigation/vertical.html", context=context)
    mobile_nav = render_to_string("navigation/mobile.html", context=context)
    side_nav = render_to_string("navigation/side.html", context=context)

    with open(TEMPLATE_OUTPUT_PATH + "base/desktop-menu.html", 'w') as fp:
        fp.write(vertical_nav)

    with open(TEMPLATE_OUTPUT_PATH + "base/nav-menu.html", 'w') as fp:
        fp.write(mobile_nav)

    with open(TEMPLATE_OUTPUT_PATH + "base/catalog-sidenav.html", 'w') as fp:
        fp.write(side_nav)


