from django.contrib import admin
from django.urls import path
from servicios.models import Productos
from servicios.utils.cargaProductos import listaProductos
from django.http import HttpResponseRedirect


class ProductosAdmin(admin.ModelAdmin):
    model = Productos
    change_list_template = "boton/productos.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('productos/', self.get_productos)]
        return my_urls + urls

    def get_productos(self, request):
        x = listaProductos()
        self.message_user(request, f'{x} productos actualizados')
        return HttpResponseRedirect("../")

    list_display = ('id',
                    'Servicio',
                    'Producto',
                    'id_servicio',
                    'id_producto',
                    'Logotipo',
                    'Imagen_Ayuda'
                    )
    search_fields = ('id_servicio',
                     'id_producto',
                     'Servicio',
                     'Producto',
                     'id_CatTipoServicio',
                     'Tipo_Front',
                     'hasDigitToVerificator',
                     )
    list_filter = ('Servicio',
                   'Producto',
                   'id_CatTipoServicio',
                   'Tipo_Front',
                   'hasDigitToVerificator',
                   'Tipo_Referencia',
                   )

    list_per_page = 40


admin.site.register(Productos, ProductosAdmin)
