from datetime import datetime
from django.utils import timezone
from ..models import Config


SUBSCRIPTION_MODE_KEY = 'subscription_mode'
SUBSCRIPTION_PAID_UNTIL_KEY = 'subscription_paid_until'


def is_subscription_mode():
    return Config.get(SUBSCRIPTION_MODE_KEY) == 'True'


def set_subscription_mode(value):
    return Config.set(SUBSCRIPTION_MODE_KEY, value)


def get_subscription_paid_until():
    value = Config.get(SUBSCRIPTION_PAID_UNTIL_KEY)
    if value:
        value = datetime.fromisoformat(value)
    return value


def set_subscription_paid_until(value):
    if value:
        value = value.isoformat()
    return Config.set(SUBSCRIPTION_PAID_UNTIL_KEY, value)


def is_subscription_valid():
    paid_until = get_subscription_paid_until()
    if paid_until and timezone.now() <= paid_until:
        return True
    return False