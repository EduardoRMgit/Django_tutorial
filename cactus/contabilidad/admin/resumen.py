from django.contrib import admin
# from contabilidad.models.resumen import Resumen


class ResumenAdmin(admin.ModelAdmin):
    list_display = ('nombre',
                    'codigo',
                    'naturaleza',
                    'saldoinicial',
                    'debe',
                    'haber',
                    'saldofinal',
                    'fecha',
                    )

    list_per_page = 25


# admin.site.register(Resumen, ResumenAdmin)
