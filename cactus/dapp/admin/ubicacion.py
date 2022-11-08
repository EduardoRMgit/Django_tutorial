from django.contrib import admin
from dapp.models import UbicacionT


class UbicacionAdmin(admin.ModelAdmin):
    model = UbicacionT
    list_display = [
        'id_mer',
        'id_cat'
    ]


admin.site.register(UbicacionT, UbicacionAdmin)
