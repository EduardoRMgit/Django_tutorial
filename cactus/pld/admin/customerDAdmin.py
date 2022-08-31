from django.contrib import admin
from pld.models import CustomerD


class CustomerDAdmin(admin.ModelAdmin):
    list_display = ('id_entidad',
                    'tipo',
                    'actividad_empresarial',
                    'sector_economico',
                    'nombre',
                    'apaterno',
                    'amaterno',
                    'actua_cuenta_propia',
                    'rfc',
                    'curp',
                    'status_code',
                    'mensaje',
                    )

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(CustomerD, CustomerDAdmin)
