from django.contrib import admin
from banca.models import Comprobante


class ComprobantesAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Comprobante._meta.fields]


admin.site.register(Comprobante, ComprobantesAdmin)
