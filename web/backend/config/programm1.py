
from django.contrib.auth.models import User

from pprint import pprint
from django.shortcuts import redirect
from social_core.exceptions import AuthAlreadyAssociated, AuthException, AuthForbidden


def registrate_user(*args, **kwargs):
    print("===========================")
    pprint(kwargs)

    email = kwargs.get('details', {}).get('email', None)
    user = kwargs.get('user', None)
    is_new = kwargs.get('is_new', None)
    if not user:
        if email:
            user, is_new = User.objects.get_or_create(
                username=email,
                email=email
            )
            return {
                "username": email,
                "user": user,
                "is_new": is_new
            }
        else:
            raise AuthException(kwargs['backend'])
    else:
        pass
    print("===========================")
