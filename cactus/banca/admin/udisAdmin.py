from django.contrib import admin
from banca.models import ValorUdis


class ValorUdisAdmin(admin.ModelAdmin):
    model = ValorUdis
    search_fields = ('balance',
                     'valor_monetario',
                     'udis_cuenta',
                     )
    list_filter = ('balance',
                   'valor_monetario',
                   'udis_cuenta',
                   )
    list_display = ('balance',
                    'valor_monetario',
                    'udis_cuenta',
                    )


admin.site.register(ValorUdis, ValorUdisAdmin)
