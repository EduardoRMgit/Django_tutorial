from django.contrib import admin
from banca.models import NivelCuenta


class NivelCuentaAdmin(admin.ModelAdmin):
    model = NivelCuenta

    fields = [f.name for f in NivelCuenta._meta.fields]
    fields.remove("id")
    list_display = fields


admin.site.register(NivelCuenta, NivelCuentaAdmin)
