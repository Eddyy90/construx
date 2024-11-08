from django.db import models
from pyUFbr.baseuf import ufbr


class Address(models.Model):
    zipcode = models.CharField(max_length=8, null=False)
    UF_CHOICES = list((uf, uf) for uf in ufbr.list_uf)
    state = models.CharField(
        max_length=2, null=False,
        choices=UF_CHOICES,
    )
    city = models.CharField(max_length=60, null=False)
    district = models.CharField(max_length=60, null=False)
    street = models.CharField(max_length=300, null=False)
    number = models.CharField(max_length=8, null=False)
    complement = models.TextField(null=True, blank=True)

    @property
    def formatted(self):
        values = [self.city, self.state, self.district, self.number, self.complement]
        values = [v for v in values if v]
        return ', '.join(values)

    def get_address_display(self):
        values = [v for v in [
            self.street,
            f'nº {self.number}',
            self.district,
            f'{self.city}/{self.state}',
            self.zipcode_display,

        ] if v]
        return ', '.join(values)

    @property
    def zipcode_display(self):
        return 'CEP {}{}{}{}{}-{}{}{}'.format(*self.zipcode)


# CEP
# Endereço,
# Nº
# Complemento
# Bairro
# Cidade
# UF