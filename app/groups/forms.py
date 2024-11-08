from typing import Any
from django import forms
from django.forms.fields import Field
from .models import Group, GroupProfile


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        labels = {
            'name': 'Nome',
        }


class GroupProfileForm(forms.ModelForm):
    name = forms.CharField(label='Nome', max_length=150)

    class Meta:
        model = GroupProfile
        fields = ('name', 'description')
        exclude = ('group',)
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }

    def get_initial_for_field(self, field: Field, field_name: str) -> Any:
        if field_name == 'name' and self.instance.pk:
            return self.instance.group.name
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance._state.adding:
            instance.group = Group()

        auth_group = instance.group
        auth_group.name = self.cleaned_data['name']
        if commit:
            auth_group.save()
            instance.save()
        return instance