from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from clients.views import edit_settings
from .api import api


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('settings/', edit_settings, name='edit_settings'),
    # allauth accounts
    path('accounts/', include('allauth.urls')),
    # home
    path('', include('misc.urls')),
    # Authentication
    path('', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('groups/', include('groups.urls')),

    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('user_notifications/', include('user_notifications.urls')),
    path('calendars/', include('calendars.urls')),
    path('schedule/', include('schedule.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
