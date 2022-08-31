from django.contrib import admin
from servicios.models import Logotypes


class LogotypesAdmin(admin.ModelAdmin):
    list_display = ('id_servicio', 'Logotipo')


admin.site.register(Logotypes, LogotypesAdmin)
