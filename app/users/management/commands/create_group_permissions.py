from django.core.management import BaseCommand
from django_tenants.utils import tenant_context
from django.contrib.auth.models import Permission
from clients.models import Client
from users.models import User
from groups.models import Group, GroupProfile


GROUPS_PERMISSIONS = {
    'Administradores': {
        User: ['add', 'change', 'delete', 'view'],
        Group: ['add', 'change', 'delete', 'view'],
    },
    'Clientes': {
        User: ['add', 'change', 'view'],
        Group: ['add', 'change', 'view'],
    },
    'Usúarios' : {
    },
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        self.create_tenant_groups()

    def create_groups(self, *args, **options):
        # Loop groups
        for group_name, group_permissions in GROUPS_PERMISSIONS.items():
            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)
            profile, created = GroupProfile.objects.get_or_create(group=group)

            # Loop models in group
            for model_cls, model_permissions in group_permissions.items():
                # Loop permissions in group/model
                for perm_name in model_permissions:
                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write(
                            "Adding " + codename + " to group " + group.__str__()
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")

    def create_tenant_groups(self):
        for tenant in Client.objects.all():
            with tenant_context(tenant):
                if tenant.is_public:
                    continue
                self.create_groups()
