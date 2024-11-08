from tkinter import ALL
from django.conf import settings
from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import auth
from django.urls import reverse

from django_tenants.utils import tenant_context

from .models import User
from clients.models import Client

ALL_AUTH_BACKEND = settings.ALL_AUTH_BACKEND


class ClientTenantMiddleware:
    def process_request(self, request):
        request.is_public = connection.schema_name == 'public'

        if request.is_public or request.user.is_authenticated:
            return

        # try to retrieve user logged on root
        root_user = None
        with tenant_context(Client.get_public()):
            root_user = auth.get_user(request)

        if not root_user or root_user.is_anonymous:
            return

        if root_user.is_superuser:
            request.root_user = root_user
            request.user = User.get_developer_user()
            return

        if not root_user.is_client:
            return

        user = User.objects.filter(
            email=root_user.email, type=User.Types.CLIENT
        ).first()
        if user:
            request.root_user = root_user
            request.user = user

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.process_request(request)
        response = self.get_response(request)
        return response
