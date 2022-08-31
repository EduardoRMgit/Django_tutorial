from django.contrib import admin
from scotiabank.models import (ScotiaDeposito)


class MovimientoDepositoAdmin(admin.ModelAdmin):

    readonly_fields = (
        'referencia_cobranza',
        'comision',
        'fecha_inicial',
        'fecha_limite',
        'indicador_forma_pago',
        'nombre_plaza_origen',
        'num_plaza_cobro',
        'num_sucursal_cobro',
        'hora_recepcion_pago',
        'fecha_presentacion_pago',
        'fecha_captura_contable',
        'fecha_aplicacion_recursos',
        'folio_registro',
        'referencias_resp',
    )
    list_display = ('get_cuentaOrdenante',
                    'get_importe',
                    'get_abono',
                    'get_comision',
                    'get_referencia',
                    'get_status',
                    'get_horaPago')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def get_comision(self, obj):
        return "$" + str(obj.comision)
    get_comision.short_description = 'Comisión'

    def get_abono(self, obj):
        return "$" + str(obj.importe_documento - obj.comision)
    get_abono.short_description = 'Importe a la cuenta del usuario'

    def get_importe(self, obj):
        return "$" + str(float(obj.importe_documento))
    get_importe.short_description = 'Importe a pagar'

    def get_cuentaOrdenante(self, obj):
        if obj.ordenante.Uprofile.cuentaClabe is not None:
            return obj.ordenante.Uprofile.cuentaClabe
        return '-'
    get_cuentaOrdenante.short_description = 'Cuenta ordenante'

    def get_horaPago(self, obj):
        if obj.fecha_presentacion_pago is not None:
            return "{} {}".format(
                obj.fecha_presentacion_pago.strftime('%d/%m/%Y'),
                obj.hora_recepcion_pago.strftime("%H:%M:%S"))
        return '-'
    get_horaPago.short_description = 'Fecha de depósito'

    def get_referencia(self, obj):
        if obj.referencia_cobranza is not None:
            return obj.referencia_cobranza
        return '-'
    get_referencia.short_description = 'Referencia de deposito'

    def get_status(self, obj):
        if obj.statusTrans is not None:
            return ScotiaDeposito.POSSIBLE_STATES[obj.statusTrans][1:]
        return '-'
    get_status.short_description = 'Estado'


admin.site.register(ScotiaDeposito, MovimientoDepositoAdmin)
