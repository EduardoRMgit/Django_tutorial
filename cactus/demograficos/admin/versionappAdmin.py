from django.contrib import admin
from demograficos.models import VersionApp


class VersionAppAdmin(admin.ModelAdmin):
    list_display = ('version',
                    'activa',
                    'url_android',
                    'url_ios',
                    'fecha')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(VersionApp, VersionAppAdmin)
