import re

from django.utils.safestring import mark_safe
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from users.models import User
from .models import (
    DOCUMENT_TYPE_CHOICES, ClientProfile, UserProfile,
)
from validate_docbr import CPF, CNPJ

cpf_validator = CPF()
cnpj_validator = CNPJ()

id_registry_widget = forms.TextInput(attrs={
    'data-inputmask': "'mask': '999.999.999-99'",
    'class': 'input-mask'
})
id_registry_field = forms.CharField(
    label='CPF', max_length=18, min_length=11,
    widget=id_registry_widget
)

id_registry_type_field = forms.ChoiceField(
    label='Tipo de Documento',
    choices=DOCUMENT_TYPE_CHOICES,
    # widget=forms.TextInput(attrs={'data-field': 'id_registry_type'})
)

phone_field = forms.CharField(
    label='Telefone', max_length=15, min_length=11,
    widget=forms.TextInput(attrs={
        'data-inputmask': "'mask': '(99) 99999-9999'",
        'class': 'input-mask'
    })
)


class IdDocumentNumberField(forms.CharField):
    """Identification Number (CPF or CNPJ)"""

    description = "String CPF or CNPJ"

    def __init__(self, id_registry_type=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id_registry_type = id_registry_type
        self.label = 'CPF'
        self.max_length = 18
        if id_registry_type == 1:
            self.label = 'CNPJ'
            self.max_length = 14
        self.widget = id_registry_widget

    def to_python(self, value):
        value = super().to_python(value)
        return re.sub(r'\D', "", value)

    def validate(self, value):
        super().validate(value)
        length = len(value)
        if length not in (11, 14):
            raise ValidationError('Documento Incompleto')
        if length == 14 and not cnpj_validator.validate(value):
            raise ValidationError('CNPJ Inválido')
        if length == 11 and not cpf_validator.validate(value):
            raise ValidationError('CPF Inválido')


class ImagePreviewWidget(forms.widgets.ClearableFileInput):
    template_name = 'users/clearable_file_input.html'

    # def render(self, name, value, attrs=[], **kwargs):
    #     attrs['class'] = 'form-control'
    #     input_html = super().render(name, value, attrs, **kwargs)
    #     img_html = ''
    #     if value:
    #        img_html = mark_safe(f'<img src="{value.url}" class="img-thumbnail" alt="Imagem de Perfil" width="200" /><br>')
    #     return f'{img_html}{input_html}'


class WorkerProfileForm(forms.ModelForm):
    id_registry = IdDocumentNumberField()
    phone_number = phone_field
    image = forms.ImageField(label="Imagem de Perfil", required=False, widget=ImagePreviewWidget)

    def clean_phone_number(self):
        new_data = re.sub(r"\D", "", self.cleaned_data['phone_number'])
        length = len(new_data)
        if length < 10 or length > 11:
            self.add_error('phone_number', "Telefone inválido")
        return new_data


class ClientProfileForm(WorkerProfileForm):
    id_registry_type = id_registry_type_field
    responsible_signature = forms.ImageField(
        label="Assinatura do(a) responsável",
        required=False,
        widget=ImagePreviewWidget,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        prefix = kwargs.get('prefix')
        id_registry_type_key = f'{prefix}-id_registry_type' if prefix else 'id_registry_type'
        if self.data.get(id_registry_type_key) == '1':
            self.fields['social_name'].required = True
            self.fields['id_registry'].max_length = 18
        else:
            self.fields['social_name'].required = False
            self.fields['id_registry'].max_length = 14
        self.fields['id_registry'].max_length = 18

    class Meta:
        model = ClientProfile
        exclude = ('user', 'address')
        labels = {
            'site_url': 'Site (URL)',
            'initials': 'Sigla',
            'id_registry_type': 'Tipo de Documento',
            'social_name': 'Razão Social',
            'responsible_name': 'Responsável',
            'responsible_signature': 'Assinatura do(a) Responsável',
            'digital': 'Escritório Digital',
        }


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'email', 'is_active', 'groups')
        labels = {
            'first_name': 'Nome Completo',
            'email': 'E-mail',
            'is_active': 'Ativo',
        }


class WorkerForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'email', 'is_active', 'groups')
        labels = {
            'first_name': 'Nome Completo',
            'email': 'E-mail',
            'is_active': 'Ativo',
        }


class UserProfileForm(WorkerProfileForm):
    class Meta():
        model = UserProfile
        exclude = ('user',)
        labels = {
            'social_name': 'Nome Completo',
            'total_access': 'Acesso Irrestrito',
            'category': 'Categoria',
        }
