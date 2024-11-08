from django.core.management.base import BaseCommand
from clients.lib import create_root_tenant


class Command(BaseCommand):
    def handle(self, **options):
        create_root_tenant()
