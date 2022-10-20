from django.contrib import admin
from dapp.models import CreatePay


class CreatepayAdmin(admin.ModelAdmin):
    model = CreatePay
    list_display = [
        'id_info',
        'user',
        'cash',
        'reference'
    ]


admin.site.register(CreatePay, CreatepayAdmin)
