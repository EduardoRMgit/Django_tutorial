from django.contrib import admin
from scotiabank.models import Archivo


class ArchivoAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'txt',
                    'get_tipo',
                    'secuencia',
                    'fecha',
                    'status',
                    'errorMsg',
                    'respuesta_FN5'
                    )

    readonly_fields = ('contenido_archivo',)

    def get_tipo(self, obj):
        return obj.tipo_archivo
    get_tipo.short_description = 'Tipo de archivo'


admin.site.register(Archivo, ArchivoAdmin)
