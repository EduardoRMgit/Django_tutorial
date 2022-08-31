from django.contrib import admin
from dde.models import DineroDeEmergencia


class DineroDeEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('id_DDE', 'user')


admin.site.register(DineroDeEmergencia, DineroDeEmergenciaAdmin)
