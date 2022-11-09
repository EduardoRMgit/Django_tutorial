from django.contrib import admin
from dapp.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = [
        'id_payment',
        'amount',
        'currency',
        'reference_num',
        'reference',
        'type',
        'type_description',
        'wallet',
        'id_wallet'
    ]


admin.site.register(Payment, PaymentAdmin)
