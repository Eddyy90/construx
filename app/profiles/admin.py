from django.contrib import admin
from .models import ClientProfile, UserProfile


admin.site.register(ClientProfile)
admin.site.register(UserProfile)