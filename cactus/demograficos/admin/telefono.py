from django.contrib import admin
from demograficos.models import TipoTelefono, ProveedorTelefonico, Telefono


class TelefonoAdmin(admin.ModelAdmin):
    list_display = ('telefono', 'user')


class TipoTelefonoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)


class ProveedorTelefonicoAdmin(admin.ModelAdmin):
    list_display = ('proveedor',
                    'country',
                    )


admin.site.register(Telefono, TelefonoAdmin)
admin.site.register(TipoTelefono, TipoTelefonoAdmin)
admin.site.register(ProveedorTelefonico, ProveedorTelefonicoAdmin)
