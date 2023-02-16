from django.contrib import admin
from pld.models import Movimiento


class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        'transaccion',
        'curp',
        'origen_pago',
        'tipo_cargo',
        'tipo_cargo_e',
        'monto_pago',
        'tipo_moneda',
        'fecha_pago',
        'payment_made_by',
        'status_code',
        'mensaje',
    )

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Movimiento, MovimientoAdmin)
