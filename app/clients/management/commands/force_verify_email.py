from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context

from clients.models import Client
from users.models import User


class Command(BaseCommand):
    def handle(self, **options):
        for tenant in Client.objects.all():
            with tenant_context(tenant):
                if tenant.is_public:
                    continue

                print(f'Forcing verify emails for: {tenant}')
                for user in User.objects.all():
                    User.force_verify_email(user)
