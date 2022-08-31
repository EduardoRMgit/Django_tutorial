from django.contrib import admin
from demograficos.admin.userPAdmin import UserProfileAdmin
from .models import Administradore, Grupo
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


class AdministradoreAdmin(UserProfileAdmin):

    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
    )

    list_filter = ()


class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ['name']


admin.site.register(Permission, PermissionAdmin)
admin.site.register(Administradore, AdministradoreAdmin)
admin.site.register(Grupo)
