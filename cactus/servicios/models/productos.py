from django.db import models
from .logos import Logotypes
from .imgRef import ImgRef
from django.utils.html import format_html


class Productos(models.Model):
    """
    ``Attributes:``

    - logotypes = many to one to the Logotypes models

    - imgref = many to one to the ImgRef models
    """

    logotypes = models.ForeignKey(
        Logotypes,
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    imgref = models.ForeignKey(
        ImgRef,
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )

    Servicio = models.CharField(max_length=100, blank=True, null=True)
    Producto = models.CharField(max_length=100, blank=True, null=True)
    id_servicio = models.IntegerField(blank=True, null=True)
    id_producto = models.IntegerField(blank=True, null=True)
    id_CatTipoServicio = models.IntegerField(blank=True, null=True)
    Tipo_Front = models.CharField(max_length=100, blank=True, null=True)
    hasDigitToVerificator = models.BooleanField(default=False, blank=True,
                                                null=True)
    Precio = models.DecimalField(blank=True, null=True,
                                 max_digits=14, decimal_places=2)
    ShowAyuda = models.BooleanField(default=True, blank=True, null=True)
    Comision = models.DecimalField(blank=True, null=True,
                                   max_digits=14, decimal_places=2)
    Tipo_Referencia = models.CharField(max_length=10, blank=True, null=True)

    def Logotipo(self):
        if self.logotypes is not None:
            return self.logotypes.Logotipo()
        else:
            url = '/media/servicios/default.png'
            return format_html(
                '<img src="{}" style="width: 45px;height:45px;"/>'.format(url))

    def Imagen_Ayuda(self):
        if self.imgref is not None:
            return self.imgref.Imagen_Ayuda()
        else:
            url = '/media/servicios/default.png'
            return format_html(
                '<img src="{}" style="width: 45px;height:45px;"/>'.format(url))

    class Meta():
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.Servicio
