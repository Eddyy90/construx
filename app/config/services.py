from clients.models import ClientSettings
from django.templatetags.static import static

class BrandingService:
    def __init__(self, client_id):
        try:
            self.settings = ClientSettings.objects.get(client_id=client_id)
        except ClientSettings.DoesNotExist:
            self.settings = None

    @property
    def name(self):
        if self.settings and self.settings.name:
            return self.settings.name
        return 'Construx'

    @property
    def logo(self):
        if self.settings and self.settings.logo:
            return self.settings.logo.url
        return static('images/brand/logo-construx.png')

    @property
    def icon(self):
        if self.settings and self.settings.logo_icon:
            return self.settings.logo_icon.url
        return static('/assets/images/brand/favicon.ico')

    @property
    def logo_small(self):
        if self.settings and self.settings.logo_small:
            return self.settings.logo_small.url
        return static('images/brand/logo-sm.png')
