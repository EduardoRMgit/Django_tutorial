from django.contrib import admin
from servicios.models import ImgRef


class ImgRefAdmin(admin.ModelAdmin):
    list_display = ('id_servicio', 'Imagen_Ayuda')


admin.site.register(ImgRef, ImgRefAdmin)
