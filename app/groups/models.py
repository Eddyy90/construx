from django.contrib.auth.models import Group
from django.db import models


class GroupProfile(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE,
        primary_key=True, related_name='profile'
    )
    description = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return "{}".format(self.name)

    @property
    def name(self):
        return self.group.name
