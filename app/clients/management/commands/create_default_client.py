from django.core.management.base import BaseCommand
from clients.lib import create_client_instance


class Command(BaseCommand):
    def handle(self, **options):
        create_client_instance(
            email='client@email.com',
            password='client',
            subdomain='client',
        )
