from django.contrib import admin
from pld.models import Movimiento


class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        'transaccion',
        "get_customer",
        'curp',
        'get_origen_pago',
        'get_tipo_cargo',
        'monto_pago',
        'tipo_moneda',
        'fecha_pago',
        'mensaje',
        'alertas'
    )

    def get_tipo_cargo(self, obj):
        return ("Enviado" if obj.tipo_cargo == 1 else "Recibido")
    get_tipo_cargo.short_description = 'Tipo cargo'

    def get_customer(self, obj):
        return (obj.customer.no_cliente if obj.customer else "-")
    get_customer.short_description = 'Customer'

    def get_origen_pago(self, obj):
        return ("Efectivo" if obj.origen_pago == 1 else "Transferencia")
    get_origen_pago.short_description = 'Origen pago'

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Movimiento, MovimientoAdmin)
