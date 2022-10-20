from django.contrib import admin
from dapp.models import RealizarP


class RealizarPAdmin(admin.ModelAdmin):
    model = RealizarP
    list_display = [
        'id_ticket',
        'id_create',
        'id_merch',
        'currency',
        'user',
        'reference',
        'id_qr',
        'date',
        'refunded',
        'id_pay',
        'id_refunds',
        'id_cat',
        'id_terminal',
        'id_cashout'
    ]


admin.site.register(RealizarP, RealizarPAdmin)
