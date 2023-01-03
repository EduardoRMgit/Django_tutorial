from django.contrib import admin
from dapp.models import Info


class InfoAdmin(admin.ModelAdmin):
    model = Info
    list_display = [
        'id_qr',
        'info',
        'id_mer',
        'id_cat',
        'id_cash'
    ]


admin.site.register(Info, InfoAdmin)
