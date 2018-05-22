from django.conf.urls import url, include

from .categories.urls import urls_categories
from .attributes.urls import urls_attributes
from .values.urls import urls_values
from .images.urls import urls_images


urls = ([
    url(r'^categories/', include(urls_categories)),
    url(r'^attributes/', include(urls_attributes)),
    url(r'^values/', include(urls_values)),
    url(r'^images/', include(urls_images)),
], 'cubes')
