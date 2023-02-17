from django.contrib import admin
from pld.models import Customer, Movimiento


class UserPLDMovimientoInline(admin.TabularInline):
    model = Movimiento
    verbose_name_plural = 'Movimientos'


class CustomerAdmin(admin.ModelAdmin):
    inlines = (UserPLDMovimientoInline,)
    list_display = ('id_entidad',
                    'tipo',
                    'nombre',
                    'actua_cuenta_propia',
                    'rfc',
                    'curp',
                    'status_code',
                    'mensaje',
                    'tienePLD',
                    )

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Customer, CustomerAdmin)
