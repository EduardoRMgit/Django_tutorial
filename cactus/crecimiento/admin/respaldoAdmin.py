from django.contrib import admin
from crecimiento.models import Respaldo


class RespaldoAdmin(admin.ModelAdmin):

    model = Respaldo

    fields = [f.name for f in Respaldo._meta.fields]
    fields.remove("id")
    list_display = fields
    list_filter = (
        'status',
        'activo'
    )
    search_fields = (
        'ordenante__username',
        'respaldo__username',
        'contacto_id'
    )


admin.site.register(Respaldo, RespaldoAdmin)
