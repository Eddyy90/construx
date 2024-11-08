from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from clients import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # auth
    path('', include('authentication.urls')),
    path('', include('authentication.register_urls')),

    # home
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('setup', views.setup, name='setup'),
    path('clients/', include('clients.urls')),
    path('users/', include('users.urls')),
    path('', include('misc.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)