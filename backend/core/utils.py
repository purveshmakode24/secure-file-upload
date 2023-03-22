from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _


def token_required(func):
    """
    Token Required decorator.
    """
    def get_user(request, *args, **kwargs):
        try:
            token_key = request.GET.get('token')

            token = Token.objects.get(key=token_key)

        except Token.DoesNotExist:
            msg = ("Not authorized to access this content. ")
            msg += ("Either the Token key as a query params is missing or is invalid.")
            return HttpResponseForbidden(msg)

        user = token.user

        return func(request, user, *args, **kwargs)

    return get_user