from django.contrib import admin
from banca.models import InguzTransaction, NotificacionCobro


class InguzTransaccionAdmin(admin.ModelAdmin):
    search_fields = ('id',
                     'monto',
                     'ordenante__username',
                     'ordenante__id',
                     )
    list_filter = (
        'statusTrans',
    )
    list_display = ('id',
                    'ordenante',
                    'monto',
                    'statusTrans',
                    'fechaOperacion',
                    'rechazada'
                    )


class NotificacionCobroAdmin(admin.ModelAdmin):

    list_filter = (
        'status',
    )

    fields = [f.name for f in NotificacionCobro._meta.fields]
    fields.remove("id")
    fields.remove("id_contacto_solicitante")
    fields.remove("concepto")
    list_display = fields


admin.site.register(InguzTransaction, InguzTransaccionAdmin)
admin.site.register(NotificacionCobro, NotificacionCobroAdmin)
