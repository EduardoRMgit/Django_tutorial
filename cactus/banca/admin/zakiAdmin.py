from django.contrib import admin
from banca.models import PagoZakiTransaccion, PrestamoZakiTransaccion

admin.site.register(PagoZakiTransaccion)
admin.site.register(PrestamoZakiTransaccion)
