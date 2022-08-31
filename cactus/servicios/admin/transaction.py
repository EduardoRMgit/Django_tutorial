from django.contrib import admin
from servicios.models import TransactionGpo


class TransactionGpoAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'owner',
                    'Fecha',
                    'Servicio',
                    'Err',
                    'Telefono',
                    'Precio',
                    )


admin.site.register(TransactionGpo, TransactionGpoAdmin)
