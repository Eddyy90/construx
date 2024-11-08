from django import forms
from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        exclude = ('created_by',)
        labels = {
            'title': 'Titulo',
            'description': 'Descrição',
            'type': 'Tipo',
            'links': 'Links',
        }
