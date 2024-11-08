from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, Permission
from .models import GroupProfile


class GroupInline(admin.StackedInline):
    model = GroupProfile
    can_delete = False
    verbose_name_plural = 'group profiles'


class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupInline, )


# Re-register GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)