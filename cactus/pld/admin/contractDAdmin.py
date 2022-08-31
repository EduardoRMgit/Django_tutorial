from django.contrib import admin
from pld.models import ContratoD


class ContratoDAdmin(admin.ModelAdmin):
    list_display = (
        'id_entidad',
        'curp',
        'rfc',
        'no_credito',
        'unidad_credito',
        'tipo_credito',
        'tipo_moneda',
        'T1',
        'T2',
        'T3',
        'T4',
        'instrumento_monetario',
        'canales_distribucion',
        'Estado',
        'status_code',
        'mensaje',
        'user',
    )

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(ContratoD, ContratoDAdmin)
