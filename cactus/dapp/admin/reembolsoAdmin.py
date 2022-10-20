from django.contrib import admin
from dapp.models import Reembolso


class ReembolsoAdmin(admin.ModelAdmin):

    list_display = ('rc',
                    'msg',
                    'user',
                    'data',
                    'security',
                    )


admin.site.register(Reembolso, ReembolsoAdmin)
