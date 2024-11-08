from django.db import models
from django.contrib.auth import get_user_model


class Work(models.Model):
    STATUS_CHOICES = (
        ("in_progress", "Em andamento"),
        ("done", "Concluida"),
        ("cancel", "Cancelada"),
    )

    name = models.CharField(max_length=120)
    init_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=120, choices=STATUS_CHOICES)
    actual_budget = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300, null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(), null=True, blank=False, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name
