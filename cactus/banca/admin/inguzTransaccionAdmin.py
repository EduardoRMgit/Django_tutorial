from django.contrib import admin
from banca.models import InguzTransaction


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


admin.site.register(InguzTransaction, InguzTransaccionAdmin)
