from django import forms
from .models import Work


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        exclude = ('created_by',)
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'type': 'Tipo',
            'init_date': 'Data de Inicio',
            'end_date': 'Data de Termino',
            'status': 'Status',
            'actual_budget': 'Orcamento Atual',
        }
