from django.db import models, connection
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.utils import tenant_context

from users.models import User



class Domain(DomainMixin):

    @classmethod
    def get_current(cls):
        return cls.objects.get(tenant=Client.get_current())


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    # paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        'users.User', null=True, blank=False, on_delete=models.PROTECT)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return f'{self.schema_name} ({self.domain})'

    @property
    def domain(self):
        domain = Domain.objects.filter(tenant=self).first()
        if domain:
            return domain.domain
        return '-'

    @classmethod
    def get_current(cls):
        return cls.objects.filter(schema_name=connection.schema_name).first()

    @classmethod
    def get_public(cls):
        return cls.objects.filter(schema_name='public').first()

    @classmethod
    def current_is_public(cls):
        return cls.get_current().is_public

    @classmethod
    def get_public_context(cls):
        return tenant_context(cls.get_public())

    @property
    def is_public(self):
        return self.schema_name == 'public'

    def get_client_user(self):
        with self.get_public_context():
            user = self.user
        with tenant_context(self):
            return User.objects.filter(email=user.email).first()


def client_file_directory_path(instance, filename):
    return 'client/{0}/{1}'.format(instance.client.id, filename)


class ClientSettings(models.Model):
    client = models.OneToOneField(
        Client, on_delete=models.CASCADE,
        primary_key=True, related_name='settings'
    )
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=client_file_directory_path, null=True, blank=True)
    logo_dark = models.ImageField(upload_to=client_file_directory_path, null=True, blank=True)
    logo_small = models.ImageField(upload_to=client_file_directory_path, null=True, blank=True)
    logo_icon = models.ImageField(upload_to=client_file_directory_path, null=True, blank=True)
