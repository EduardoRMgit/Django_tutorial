from django.contrib import admin
from dapp.models import CodigoCobro


class CodigoAdmin(admin.ModelAdmin):

    list_display = ('user',
                    'code',
                    'security',
                    )


admin.site.register(CodigoCobro, CodigoAdmin)
