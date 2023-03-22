from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import AuthTokenSerializer, UserCreateSerializer
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response

# Create your views here.

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    A viewset for registering user.
    """
    serializer_class = UserCreateSerializer
    queryset = get_user_model().objects.all()
