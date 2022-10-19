from django.contrib import admin
from dapp.models import CashoutM


class CashoutAdmin(admin.ModelAdmin):
    model = CashoutM
    list_display = [
        'id_cashout',
        'amount',
        'currency'
    ]


admin.site.register(CashoutM, CashoutAdmin)
