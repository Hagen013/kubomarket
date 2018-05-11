from elasticsearch_dsl import (
    DocType,
    Date,
    Keyword,
    Text,
    Boolean,
    Integer,
    Nested
)

from config.es_client import es_client


class CategoryIndex(DocType):

    class Meta:
        index = 'store'
        doc_type = 'category'
        using = es_client

    id = Integer()
    name = Text()
    absolute_url = Text()
    search_scoring = Integer()


class ProductCardIndex(DocType):

    class Meta:
        index = 'store'
        doc_type = 'product'
        using = es_client

    id = Integer()
    offer_identifier = Text()
    name = Text()
    absolute_url = Text()
    price = Integer()
    vendor = Text()
    description = Text()
    vendor_code = Text()

