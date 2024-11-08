from django.conf import settings
from django.core import management
from django.utils.text import slugify
from django_tenants.utils import tenant_context

from users.models import User
from clients.models import Client, Domain

SITE_DOMAIN = settings.SITE_DOMAIN


def create_root_tenant():
    tenant = Client(
        schema_name='public',
        name='Public Schema',
        on_trial=False,
    )
    tenant.save()
    domain = Domain(
        domain=settings.SITE_DOMAIN,
        tenant=tenant,
        is_primary=True,
    )
    domain.save()

    return tenant


def format_subdomain(subdomain):
    return slugify(subdomain).replace('_', '-')

def format_domain(subdomain):
    return f'{subdomain}.c.{SITE_DOMAIN}'


def create_user_tenant(user, subdomain=None):
    if not subdomain:
        username = user.email.split('@')[0]
        subdomain = format_subdomain(username)
    domain_url = format_domain(subdomain)

    tenant = Client(
        user=user,
        schema_name=f'tenant_{user.id}',
        name='User Schema',
        on_trial=False,
    )
    tenant.save()
    domain = Domain(
        domain=domain_url,
        tenant=tenant,
        is_primary=True,
    )
    domain.save()
    return tenant


def create_super_user():
    super_user = User.objects.create_superuser(
        settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD,
        type=User.Types.ADMIN
    )
    super_user.save()
    User.force_verify_email(super_user)


def create_client_instance(email, password, subdomain):
    user = User.objects.create(email=email, password=password, type=User.Types.CLIENT)
    user.save()
    User.force_verify_email(user)
    client = create_user_tenant(user, subdomain)
    setup_user_tenant(client)


def setup_user_tenant(client):
    """Create initial models for a Tenant instance"""
    user = client.user
    if user.type != User.Types.CLIENT:
        return

    with tenant_context(client):
        create_super_user()
        user.id = None
        user.save()
        User.force_verify_email(user)

        # Wallet.objects.create(user=user)

        management.call_command("create_group_permissions")
        management.call_command(
            "loaddata",
            "document_model/fixtures/initial.json",
            "process_types/fixtures/initial.json",
        )
        management.call_command("generate_thumbnail")
