from django.contrib import admin
from pld.models import adminUtils


class adminUtilsAdmin(admin.ModelAdmin):
    list_display = ('util', 'activo')
    list_editable = ('activo',)


admin.site.register(adminUtils, adminUtilsAdmin)
