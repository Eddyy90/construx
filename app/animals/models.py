from django.db import models
from django.contrib.auth import get_user_model


class Animal(models.Model):
    
    name = models.CharField(max_length=120)
    birth_date = models.DateField()
    race = models.CharField(max_length=120)
    gender = models.CharField(max_length=120)
    history = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(), null=True, blank=False, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name
