from django.contrib import admin
from demograficos.models import adminUtils, UserProfile
from django.utils import timezone


class adminUtilsAdmin(admin.ModelAdmin):
    list_display = ('util', 'activo')
    list_editable = ('activo',)


def set_blocked(modeladmin, request, queryset):
    queryset.update(status='B')
    queryset.update(blocked_date=timezone.now())


def set_unblocked(modeladmin, request, queryset):
    queryset.update(status='O')


set_blocked.short_description = "Block user"
set_unblocked.short_description = "Unblock user"


class UPAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'blocked_date']
    ordering = ['user']
    actions = [set_blocked, set_unblocked]


admin.site.register(UserProfile, UPAdmin)
admin.site.register(adminUtils, adminUtilsAdmin)
