from django.contrib import admin
from scotiabank.models import ScotiaRetiro
from scotiabank.utility.ScotiaUtil import GeneraRetiro


class MovimientoRetiroAdmin(admin.ModelAdmin):

    actions = ['generar_archivo_retiro']
    readonly_fields = (
        'clave_retiro',
        'referenciaPago',
        'archivo',
        'archivo_respuesta_FN2',
        'archivo_resumen',
        'comision'
    )
    list_display = ('get_concepto',
                    'get_monto',
                    'saldoReservado',
                    'clave_retiro',
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

    def generar_archivo_retiro(self, request, movimientos):
        """ Generacion de archivo TXT de intercambio. """

        mensaje = GeneraRetiro(movimientos)
        self.message_user(request, mensaje)
    generar_archivo_retiro.short_description = "Generar archivo."


admin.site.register(ScotiaRetiro, MovimientoRetiroAdmin)
