from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django_tenants.utils import schema_exists
from .models import Client, Domain, ClientSettings
from .lib import format_domain, format_subdomain


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ('domain',)
        labels = {
            'domain': 'Subdomínio',
        }

    def clean_domain(self):
        domain = self.cleaned_data["domain"]
        domain = format_subdomain(domain)
        domain_url = format_domain(domain)
        if Domain.objects.filter(domain=domain_url).all():
            raise ValidationError("Esse subdomínio já está em uso")
        else:
            return domain


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('schema_name',)
        labels = {
            'schema_name': 'Nome do Schema',
        }

    def clean_schema_name(self):
        schema_name = self.cleaned_data["schema_name"]
        schema_name = slugify(schema_name).replace("-", "")
        schema_name = slugify(schema_name).replace(".", "")
        if schema_exists(schema_name):
            raise ValidationError("A schema with this name already exists in the database")
        else:
            return schema_name


# Create and change images form

class ClientSettingsForm(forms.ModelForm):
    class Meta:
        model = ClientSettings
        exclude = ['client']
        labels  = {
            'name': 'Nome',
            'logo': 'Logo',
            'logo_dark': 'Logo (Dark Mode)',
            'logo_small': 'Logo (Pequena)',
            'logo_icon': 'Ícone',
        }
