from django.contrib import admin
from pld.models import UrlsPLD


class UrlsPLDAdmin(admin.ModelAdmin):
    list_display = ('urls',
                    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(UrlsPLD, UrlsPLDAdmin)
