from django.contrib import admin
from pld.models import MovimientoD


class MovimientoDAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'id_entidad',
        'id_credito',
        'origen_pago',
        'tipo_cargo',
        'tipo_cargo_e',
        'monto_pago',
        'tipo_moneda',
        'fecha_pago',
        'comentarios',
        'cuenta',
        'created_at',
        'payment_made_by',
        'status_code',
        'mensaje',
    )

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MovimientoD, MovimientoDAdmin)
