from demograficos.models import PerfilTransaccionalDeclarado

from django.contrib import admin


class PerfilTransaccionalDeclaradoAdmin(admin.ModelAdmin):

    model = PerfilTransaccionalDeclarado

    fields = [f.name for f in PerfilTransaccionalDeclarado._meta.fields]
    fields.remove("id")
    list_display = fields


admin.site.register(PerfilTransaccionalDeclarado,
                    PerfilTransaccionalDeclaradoAdmin)
