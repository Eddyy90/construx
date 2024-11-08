from django.conf import settings
from config.services import BrandingService

def general_info(request):
    return {
        'support_url': settings.SUPPORT_URL,
    }


def branding(request):
    if hasattr(request, 'tenant') and request.tenant:
        return {'branding': BrandingService(request.tenant.id)}
    return {}