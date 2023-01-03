from django.contrib import admin
from dapp.models import Qr


class QrAdmin(admin.ModelAdmin):
    model = Qr
    list_display = [
        'qr',
        'description',
        'amount',
        'currency',
        'reference_num'
    ]


admin.site.register(Qr, QrAdmin)
