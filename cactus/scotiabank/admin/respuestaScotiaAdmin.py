from django.contrib import admin
from scotiabank.models import RespuestaScotia


class RespuestaScotiaAdmin(admin.ModelAdmin):
    list_display = ('tipo',
                    'nombre_archivo', 'fecha', 'url_respuesta')
    list_display_links = ('nombre_archivo',)
    readonly_fields = ('fecha', 'nombre_archivo', 'tipo', 'contenido')


admin.site.register(RespuestaScotia, RespuestaScotiaAdmin)
