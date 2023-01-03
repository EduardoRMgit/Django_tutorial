from django.contrib import admin
from demograficos.models.telefono import (TipoTelefono,
                                          ProveedorTelefonico,
                                          Telefono,
                                          PhoneVerification)


class PhoneVeriicationAdmin(admin.ModelAdmin):
    search_fields = ('token',
                     'ssid',
                     'fechaCreacion',
                     'telefono',
                     )

    list_filter = ('token',
                   'ssid',
                   'fechaCreacion',
                   )

    list_display = ('token',
                    'ssid',
                    'fechaCreacion',
                    'telefono',
                    )

    list_per_page = 25

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PhoneVeriicationline(admin.TabularInline):
    model = PhoneVerification
    can_delete = False
    verbose_name_plural = 'Mensajes Enviados'
    fk_name = 'telefono'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TelefonoAdmin(admin.ModelAdmin):
    inlines = (
        PhoneVeriicationline,
    )

    search_fields = ('telefono',
                     )

    list_filter = ('country',
                   'activo',
                   'validado',
                   'proveedorTelefonico',
                   'tipoTelefono',
                   )

    list_display = ('telefono',
                    'extension',
                    'fechaCreacion',
                    'country',
                    'prefijo',
                    'activo',
                    'validado',
                    'user',
                    'proveedorTelefonico',
                    'tipoTelefono',
                    'get_ssid',
                    )

    def get_ssid(self, obj):
        try:
            ssids = ""
            for pvTel in obj.PVTelefono.all():
                ssids += pvTel.ssid
                ssids += " \n"
            return ssids
        except Exception:
            return None
    get_ssid.short_description = 'SSID'

    list_per_page = 25


admin.site.register(Telefono, TelefonoAdmin)
admin.site.register(ProveedorTelefonico)
admin.site.register(TipoTelefono)
admin.site.register(PhoneVerification, PhoneVeriicationAdmin)
