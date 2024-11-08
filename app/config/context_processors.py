from .lib.subscription import (
    is_subscription_mode,
    is_subscription_valid,
)


def subscription_mode(request):
    if request.is_public or request.user.is_anonymous:
        return {
            'subscription_mode': False,
            'subscription_expired': False,
        }

    return {
        'subscription_mode': is_subscription_mode(),
        'is_subscription_valid': is_subscription_valid(),
    }