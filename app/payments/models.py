from django.db import models
from django.contrib.auth import get_user_model

STATUS_CHOICES = (
    ("pending", "Pendente"),
    ("paid", "Pago"),
    ("cancelled", "Cancelado"),
)
class Payment(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300, null=True, blank=True)
    value = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False, default=0.00
    )
    
    payment_date = models.DateField(null=False, blank=False)
    status = models.CharField(
        max_length=120, null=False, blank=False, choices=STATUS_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(), null=True, blank=False, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name
