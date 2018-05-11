from django.db import models
from django.core.validators import RegexValidator


class DisplayableURLField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["verbose_name"] = "URL"
        kwargs["max_length"] = 2048
        kwargs["editable"] = False
        kwargs["unique"] = True
        kwargs["validators"] = [
                RegexValidator(
                    regex=r'^(($)|(([-_\da-z]+/)+$))',
                    message='slug valid error',
                )
            ]
        super(DisplayableURLField, self).__init__(*args, **kwargs)
