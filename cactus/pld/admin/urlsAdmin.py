from django.contrib import admin
from pld.models import UrlsPLD


class UrlsPLDAdmin(admin.ModelAdmin):
    
    fields = [f.name for f in UrlsPLD._meta.fields]
    fields.remove("id")
    list_display = fields

    def has_delete_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(UrlsPLD, UrlsPLDAdmin)
