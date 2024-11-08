from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'groups')
        labels = {
            'first_name': 'Nome Completo',
            'email': 'E-mail',
            'groups': 'Grupos',
        }


class ImpersonateForm(forms.Form):
    profile = forms.ModelChoiceField(required=False, queryset=User.objects.all())
