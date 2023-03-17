from django.contrib import admin
from pld.models import AlertasPLD


class AlertasAdmin(admin.ModelAdmin):
    list_display = ('descripcion',
                    'fecha',
                    'motivo'
                    )


admin.site.register(AlertasPLD, AlertasAdmin)
