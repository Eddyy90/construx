import re
from django import forms
from crispy_forms.helper import FormHelper
from .models import Address 


zipcode_field = forms.CharField(label='CEP', max_length=9, min_length=8,
                                widget=forms.TextInput(attrs={
                                    'data-inputmask': "'mask': '99999-999'",
                                    'class': 'input-mask zipcode-field'}))

class AddressForm(forms.ModelForm):
    zipcode = zipcode_field

    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'zipcode': 'CEP',
            'street': 'Rua',
            'number': 'Número',
            'complement': 'Complemento',
            'state': 'UF',
            'city': 'Cidade',
            'district': 'Bairro',
        }


    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


    def clean_zipcode(self):
        new_data = re.sub(r"\D", "", self.cleaned_data['zipcode'])
        if len(new_data) != 8:
            self.add_error('zipcode', "CEP Inválido")
        return new_data

    # def save(self, commit=True):
    #     qualification_level = super().save(commit=False)
    #     qualification_level.user_id = request.user.id
    #     if commit:
    #         qualification_level.save()
    #     return qualification_level 
