from django.db import models
from django_countries.fields import CountryField
from demograficos.models.instituciones import Institucion
from django.utils import timezone


class CarProducto(models.Model):
    """
        Solo funciona si el producto es Dinero de Emergencia.
    """
    nombre = models.CharField('Nombre', max_length=20)
    numDiasCobro = models.IntegerField('Dias para Cobro')
    diasVencimiento = models.IntegerField('Dias Para Vencer')
    diasIncobrable = models.IntegerField('Dias Para Incobrable')
    porcentajeComision = models.DecimalField(
        '% Comision',
        max_digits=30,
        decimal_places=4,
        default=0.12
    )
    porcentajeIVA = models.DecimalField(
        '% Iva de Comision',
        max_digits=30,
        decimal_places=4,
        default=0.16
    )
    activo = models.BooleanField(default=True)
    pub_date = models.DateTimeField('Fecha Creacion', default=timezone.now)

    class Meta():
        verbose_name_plural = 'Caracteristicas de Productos'

    def __str__(self):
        return self.nombre


class PaisesDisponibles(models.Model):
    paises = CountryField()


class Productos(models.Model):
    producto = models.CharField(max_length=50)
    paises_disponibles = models.ManyToManyField(PaisesDisponibles)
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    reglasVencimiento = models.ForeignKey(
        CarProducto,
        on_delete=models.PROTECT,
        related_name='carProducto_producto',
        blank=True,
        null=True
    )

    class Meta():
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.producto
