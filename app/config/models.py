from django.db import models


_DEFAULTS = {}


class Config(models.Model):
    key = models.CharField(max_length=255, null=False, unique=True)
    value = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.key

    @classmethod
    def set(cls, key, value):
        """Set a value for a Config."""
        config = cls.objects.filter(key=key)
        if not config:
            config = cls.objects.create(key=key, value=value)
        else:
            config.value = value
            config.save()

    @classmethod
    def get(cls, key, default=None):
        """Get a value for a Config."""
        config = cls.objects.filter(key=key).first()
        if config:
            return config.value
        return default

    @classmethod
    def get_int(cls, key):
        """Get a int value for a Config."""
        value = cls.get(key)
        if value:
            int(value)