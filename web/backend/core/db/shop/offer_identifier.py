import re
from collections import namedtuple

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType


class OfferIdentifier(namedtuple('OfferIdentifier',
                                 ['app_label',
                                  'model_name',
                                  'offer_id'])):

    """
    Класс-контракт для передачи ссылку на предложение

    app_label : str
    model_name : str
    offer_id : int

    BaseOffer может использоваться как примесь и как полноценный офер.
    (модификация товара (красные штаны)). Класс OfferIdentifier необходим,
    для передачи офера между различными приложениями.
    """

    __slots__ = ()
    # формат представления в виде строки идентификатора
    RE = re.compile("^[-_a-z]+__[-_a-z]+__[\d]+$")

    def __str__(self):
        return str('__'.join((self.app_label,
                              self.model_name,
                              str(self.offer_id),
                              ))
                   )

    @classmethod
    def from_str(cls, str_offer_identifier):
        app_label, model_name, offer_id = str_offer_identifier.split('__')
        return(cls(app_label, model_name, int(offer_id)))

    def __iter__(self):
        """
        Необходимо для приведения к dict()
        """
        yield 'app_label', self.app_label,
        yield 'model_name', self.model_name
        yield 'offer_id', self.offer_id

    def get(self):
        return ContentType.\
            objects.\
            get_by_natural_key(self.app_label, self.model_name).\
            model_class().objects.\
            get(id=self.offer_id)

    def clean(self):
        if not re.fullmatch(self.RE, str(self)):
            msg = "OfferIdentifier invalid identifier {0}".format(str(self))
            raise ValidationError(msg)
        if not all(((type(self.app_label) is str),
                    (type(self.model_name) is str),
                    (type(self.offer_id) is int))):
            msg = "OfferIdentifier invalid data types {0}".format(str(self))
            raise ValidationError(msg)
