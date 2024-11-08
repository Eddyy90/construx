import os

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
# from django_tenants.utils import parse_tenant_config_path
from django.db import connection


def parse_tenant_config_path(config_path):
    try:
        # Insert schema name
        return config_path % connection.schema_name
    except (TypeError, ValueError):
        # No %s in string; append schema name at the end
        return os.path.join(config_path, connection.schema_name)


class TenantS3Storage(S3Boto3Storage):

    @property
    def location(self):
        _location = parse_tenant_config_path(
            settings.AWS_PRIVATE_MEDIA_LOCATION)
        return _location