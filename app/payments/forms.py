from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('created_by',)
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'type': 'Tipo',
            'value': 'Valor',
            'payment_date': 'Data do Pagamento',
            'status': 'Status do Pagamento',
        }
