from django.contrib import admin
from scotiabank.models import ScotiaTransferencia
from scotiabank.utility.ScotiaUtil import GeneraTransferencia


class MovimientoTransaccionAdmin(admin.ModelAdmin):

    actions = ['generar_archivo_transaccion']
    readonly_fields = ('archivo', 'archivo_respuesta_FN2',
                       'archivo_respuesta_FN5', 'archivo_resumen',
                       'status_codigo',
                       'tipo_trans',
                       'comision')
    list_display = ('get_concepto',
                    'get_monto',
                    'get_archivo',
                    'get_archivo_secuencia',
                    'statusTrans')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def get_archivo(self, obj):
        return obj.archivo
    get_archivo.short_description = 'archivo'

    def get_monto(self, obj):
        return obj.monto
    get_monto.short_description = 'monto'

    def get_concepto(self, obj):
        if obj.transaccion is not None:
            return obj.conceptoPago
        return '-'
    get_concepto.short_description = 'concepto'

    def get_archivo_secuencia(self, obj):
        if obj.archivo is not None:
            return obj.archivo.secuencia
        return '-'
    get_archivo_secuencia.short_description = 'sencuencia de archivo'

    def generar_archivo_transaccion(self, request, movimientos):
        """ Generacion de archivo TXT de intercambio. """
        mensaje = GeneraTransferencia(movimientos)
        self.message_user(request, mensaje)
    generar_archivo_transaccion.short_description = "Generar archivo."


admin.site.register(ScotiaTransferencia, MovimientoTransaccionAdmin)
