from django.core.management.base import BaseCommand
from clients.lib import create_super_user


class Command(BaseCommand):
    def handle(self, **options):
        create_super_user()
