from ast import Interactive
from django.apps import AppConfig


class SetupConfig(AppConfig):
    name = 'construx.setup'

    def ready(self):
        from django.core import management

        management.call_command(
            "migrate_schemas",
            interactive=False,
        )

        management.call_command(
            "collectstatic",
            interactive=False
        )
