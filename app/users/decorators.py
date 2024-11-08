from tabnanny import check
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def check_client_status(user):
    if not user.is_authenticated or user.is_anonymous:
        return False
    return user.is_client or user.is_admin,


def check_admin_status(user):
    if not user.is_authenticated or user.is_anonymous:
        return False
    return user.is_admin,


def client_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the logged in user is at least client in hierarchy,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        check_client_status,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the logged in user is admin,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        check_admin_status,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
