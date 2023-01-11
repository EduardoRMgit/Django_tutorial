from demograficos.models import PerfilTransaccionalDeclarado

from django.contrib import admin


class PerfilTransaccionalDeclaradoAdmin(admin.ModelAdmin):

    model = PerfilTransaccionalDeclarado

    list_display = ('id',
                    'user',
                    'status_perfil',)


admin.site.register(PerfilTransaccionalDeclarado,
                    PerfilTransaccionalDeclaradoAdmin)
