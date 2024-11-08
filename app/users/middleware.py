import logging
from django.contrib import messages
from django.urls import reverse

from .models import User


class ImpersonateMiddleware:
    def process_request(self, request):
        if request.path.startswith('/admin'):
            return
        if request.user.is_superuser and 'impersonate_id' in request.session:
            request.original_user = request.user
            request.user = User.objects.get(id=request.session['impersonate_id'])
            # unimpersonate_url = reverse('profile_unimpersonate')
            # messages.warning(
            #     request,
            #     f'Você está personificado como usuário <strong>{request.user.first_name or request.user.email}</strong>. Para despersonificar, clique <a href="{unimpersonate_url}">aqui</a>',
            #     extra_tags='safe',
            # )

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.process_request(request)
        response = self.get_response(request)
        return response