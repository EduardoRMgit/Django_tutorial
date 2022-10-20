from django.contrib import admin
from dapp.models import Merchant


class MerchantAdmin(admin.ModelAdmin):
    model = Merchant
    list_display = [
        'merchant',
        'name',
        'address',
        'image',
        'latitude',
        'longitude',
        'phone',
        'type'
    ]


admin.site.register(Merchant, MerchantAdmin)
