from django.contrib import admin
from demograficos.models import Contacto


class ContactoAdmin(admin.ModelAdmin):
    model = Contacto
    list_display = ('nombre',
                    'ap_paterno',
                    'ap_materno',
                    'banco',
                    'clabe',
                    'activo',
                    'verificacion',
                    'user',
                    )
    list_filter = ('banco',
                   'verificacion',
                   'user',
                   )
    search_fields = ('clabe', 'nombre')


admin.site.register(Contacto, ContactoAdmin)
