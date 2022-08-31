from django.contrib import admin
from banca.models.transaccion import StatusTrans
from banca.models.catalogos import (TipoTransaccion,
                                    Comision)
from banca.models.entidades import CodigoConfianza


admin.site.register(StatusTrans)
admin.site.register(TipoTransaccion)
admin.site.register(CodigoConfianza)


class ComisionAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'monto', 'tipo',)
    list_filter = ('tipo',)


admin.site.register(Comision, ComisionAdmin)
