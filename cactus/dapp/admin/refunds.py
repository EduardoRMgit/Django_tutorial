from django.contrib import admin

from dapp.models import Refund


class RefundAdmin(admin.ModelAdmin):
    model = Refund
    list_display = [
        'id_refunds',
        'amount',
        'currency',
        'date'
    ]


admin.site.register(Refund, RefundAdmin)
