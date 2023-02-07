from django.contrib import admin
from crecimiento.models import Bartola


class BartolaAdmin(admin.ModelAdmin):

    model = Bartola

    fields = [f.name for f in Bartola._meta.fields]
    fields.remove("id")
    fields.remove("descripcion")
    list_display = fields
    search_fields = (
        'nombre',
    )


admin.site.register(Bartola, BartolaAdmin)
