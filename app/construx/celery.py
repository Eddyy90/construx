from os import environ

environ.setdefault('DJANGO_SETTINGS_MODULE', 'construx.settings')

from tenant_schemas_celery.app import CeleryApp
from django.conf import settings


# production = environ.get('PRODUCTION') is not None
connection = environ.get('RABBITMQ_IP') or "localhost"
redis_ip = environ.get('REDIS_IP') or "localhost"
redis_url = f'redis://{redis_ip}:6379/1'
app = CeleryApp(
    'construx',
    broker=f'amqp://guest@{connection}//',
    backend=redis_url,
)

# app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.conf.worker_max_tasks_per_child = 1
app.conf.worker_max_memory_per_child = 3400 * 1000 # 3GB
app.conf.worker_concurrency = 1
app.conf.redbeat_redis_url = redis_url

# app.autodiscover_tasks(['document', 'digitization', 'user_notifications'])
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)