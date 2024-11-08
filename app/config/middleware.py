from django.contrib import messages
from django.urls import reverse

from .lib.subscription import (
    is_subscription_mode,
    is_subscription_valid,
)


class ConfigMiddleware:
    def process_request(self, request):
        if not request.is_public and not request.user.is_anonymous:
            if is_subscription_mode() and not is_subscription_valid():
                messages.warning(
                    request,
                    f'A mensalidade do sistema está vencida. Por favor efetuar pagamento',
                    extra_tags='safe',
                )

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.process_request(request)
        response = self.get_response(request)
        return response
