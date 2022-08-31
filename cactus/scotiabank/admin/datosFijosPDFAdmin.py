from django.contrib import admin
from scotiabank.models import DatosFijosPDF


class DatosFijosPDFAdmin(admin.ModelAdmin):
    list_display = ("tipo_transaccion",)


admin.site.register(DatosFijosPDF, DatosFijosPDFAdmin)
